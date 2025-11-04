# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

# TODO: Testing


from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.utils.html import format_html


from .models import Category, Entry, GroupProfile

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exlude = None

    def get_queryset(self, request) -> QuerySet[Category]:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # TODO: Make sure, this works also without groups
        # TODO: Better queryset
        return get_allowed_categories(request.user, qs)


def get_allowed_categories(
    user, queryset: QuerySet[Category] | None = None
) -> QuerySet[Category]:
    branchqs = Category.objects.none()
    for group in user.groups.all():
        branchqs = branchqs.union(group.groupprofile.categories.all())

    cats = get_categorybranch(branchqs)
    if not queryset:
        queryset = Category.objects.all()
    return queryset.filter(id__in=cats)


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
        pks.add(cat.id)
        subcats = get_categorybranch(cat.subcategories.all())
        pks = pks.union(subcats)
    return pks


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    fields = [
        ("title", "category"),
        ("creation_time", "update_time"),
        "status",
        "published",
        "description",
        "email",
        ("latitude", "longitude"),
        ("image", "image_preview"),
    ]
    readonly_fields = [
        "image_preview",
        "creation_time",
        "update_time",
    ]

    def image_preview(self, obj: Entry) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return ""

    image_preview.short_description = "Preview"

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
