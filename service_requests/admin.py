# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.contrib import admin

from service_requests.models import ServiceRequest

# Register your models here.


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    exlude = None
