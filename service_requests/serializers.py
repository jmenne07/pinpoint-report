# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from rest_framework import serializers

from service_requests.models import ServiceRequest


class ServiceRequestSerializer(serializers.Serializer):
    class Meta:
        model: ServiceRequest
