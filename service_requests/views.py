# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.http import HttpResponse
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer

# Create your views here.


def index(request):
    return HttpResponse(b"Dies ist ein Test.")


class ServiceRequestList(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()  # type: ignore
    serializer_class = ServiceRequestSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]


class ServiceRequestDetails(generics.RetrieveAPIView):
    queryset = ServiceRequest.objects.all()  # type: ignore
    serializer_class = ServiceRequestSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
