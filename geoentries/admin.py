# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

# TODO: Testing


from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from simple_history.admin import SimpleHistoryAdmin

from .models import Category, Entry, GroupProfile, Mail

# Register your models here.


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    exlude = None
    mptt_level_indent = 20

    def get_queryset(self, request) -> QuerySet[Category]:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # TODO: Make sure, this works also without groups
        # TODO: Better queryset
        return get_allowed_categories(request.user, qs)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if obj and not obj.email and not request.user.is_superuser:
            fields = [f for f in fields if f != "extern"]
        return fields


def get_allowed_categories(
    user, queryset: QuerySet[Category] | None = None
) -> QuerySet[Category]:
    branchqs = Category.objects.none()
    for group in user.groups.all():
        try:
            branchqs = branchqs.union(group.groupprofile.categories.all())
        except Exception as e:
            print(e)

    cats = get_categorybranch(branchqs)
    if not queryset:
        queryset = Category.objects.all()
    return queryset.filter(name__in=cats)


def get_categorybranch(queryset: QuerySet[Category]) -> set[int]:
    """
    A function to get all ids of Category branches

    Arguments:

        queryset: QuerySet[Category]
            A set of Categories, for which the subcategories should be known

    Returns: Set[int]
        A set of integer, which contains every id of categories in the initial queryset and their subcategories.
    """
    pks = set()
    # TODO: Refactor the warning
    if queryset.model != Category:
        print("Warning")
    for cat in queryset:
        # pks.add(cat.id)
        pks.add(cat.name)
        subcats = get_categorybranch(cat.subcategories.all())
        pks = pks.union(subcats)
    return pks


class CategoryFilter(TreeRelatedFieldListFilter):
    """
    Custom filter, which modifies the field_choices of a TreeRelatedFieldListFilter

    The modification makes it so, that only Category are shown, which the user can access
    """

    def field_choices(self, field, request, model_admin):
        sfc = super().field_choices(field, request, model_admin)
        if request.user.is_superuser:
            return sfc
        cats = get_allowed_categories(request.user)
        fc = []
        catnames = set()
        for cat in cats:
            catnames.add(cat.name)
        for x in sfc:
            if x[0] in catnames:
                fc.append(x)
        return fc


@admin.register(Entry)
class EntryAdmin(SimpleHistoryAdmin):
    fields = [
        ("title", "category"),
        ("creation_time", "update_time"),
        "status",
        "published",
        "description",
        "email",
        ("latitude", "longitude", "map"),
        ("image", "image_preview"),
    ]
    readonly_fields = [
        "image_preview",
        "creation_time",
        "update_time",
        "map",
    ]

    list_filter = [
        "status",
        ("category", CategoryFilter),
        "creation_time",
        "published",
    ]
    list_display = ["__str__", "status", "published", "creation_time", "category"]

    history_list_display = ["status"]

    def image_preview(self, obj: Entry) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return ""

    image_preview.short_description = "Preview"

    def map(self, obj):
        if not obj.latitude or not obj.longitude:
            return "No location available."

        div_id = f"map_{obj.pk}"

        return mark_safe(f"""
            <div id="{div_id}" style="height: 300px; width: 300px; border:1px solid #ccc;"></div>

            <script>
            (function() {{

                function initLeafletMap() {{
                    // Ensure Leaflet is loaded
                    if (typeof L === "undefined") {{
                        return setTimeout(initLeafletMap, 100);
                    }}

                    var container = L.DomUtil.get("{div_id}");

                    // Prevent double initialization
                    if (container._leaflet_id) {{
                        return;
                    }}

                    var map = L.map("{div_id}").setView([{obj.latitude}, {obj.longitude}], 13);

                    L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
                        maxZoom: 19
                    }}).addTo(map);

                    L.marker([{obj.latitude}, {obj.longitude}]).addTo(map);
                }}

                // Run once after page load
                window.addEventListener("load", initLeafletMap);

                // Run again after Django admin inline/fieldset interactions
                document.addEventListener("DOMContentLoaded", initLeafletMap);

                // Admin sometimes triggers re-renders; check again after 500ms
                setTimeout(initLeafletMap, 500);

            }})();
            </script>
        """)

    class Media:
        css = {"all": ("https://unpkg.com/leaflet/dist/leaflet.css",)}
        js = ("https://unpkg.com/leaflet/dist/leaflet.js",)

    def get_queryset(self, request) -> QuerySet[Entry]:
        # TODO: Make sure this works without groups
        # TODO: Better queryset
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        cats = get_allowed_categories(request.user)

        return qs.filter(category__in=cats)


admin.site.unregister(Group)


class GroupInline(admin.StackedInline):
    model = GroupProfile
    filter_horizontal = ["categories"]
    can_delete = False


@admin.register(Group)
class MyGroupAdmin(GroupAdmin):
    exclude = None
    inlines = [GroupInline]


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    exlcude = None


admin.site.site_header = "Pinpoint-Admin"
admin.site.site_title = "Pinpoint Administration"
admin.site.index_title = "Wilkommen zum Admin-Dashboard"
