# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.contrib import admin

from .models import Entry

# Register your models here.


@admin.register(Entry)
class ServiceRequestAdmin(admin.ModelAdmin):
    exlude = None
