# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from http.client import HTTPResponse

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ServiceRequest
from .serializers import ServiceRequestSerializer


from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
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
    # renderer_classes = [JSONRenderer, XMLRenderer, BrowsableAPIRenderer]
