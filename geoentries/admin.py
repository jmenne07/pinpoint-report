# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

# TODO: Testing


from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Entry

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exlude = None


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
