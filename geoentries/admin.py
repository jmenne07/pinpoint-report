# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.contrib import admin

from .models import Category, Entry

# Register your models here.


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    exlude = None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exlude = None
