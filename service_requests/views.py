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

# Create your views here.


def index(request):
    return HttpResponse(b"Dies ist ein Test.")


class ServiceRequestList(generics.ListCreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
