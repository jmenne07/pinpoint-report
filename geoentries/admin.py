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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # TODO: Make sure, this works also without groups
        # TODO: Better queryset
        branchqs = request.user.groups.first().groupprofile.categories.all()
        import pdb

        pdb.set_trace()
        branch = get_categorybranch(branchqs)
        qs = qs.filter(id__in=branch)
        return qs


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

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return ""

    image_preview.short_description = "Preview"

    def get_queryset(self, request):
        # TODO: Make sure this works without groups
        # TODO: Better queryset
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        cats = request.user.groups.first().groupprofile.categories.all()

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
