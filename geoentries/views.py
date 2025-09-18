# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.http import HttpResponse
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from .models import Entry, Category
from .serializers import CategorySerializer, EntrySerializer

# Create your views here.


def index(request):
    return HttpResponse(b"Dies ist ein Test.")


class EntryList(generics.ListCreateAPIView):
    queryset = Entry.objects.all()  # type: ignore
    serializer_class = EntrySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["id", "category", "status"]


# NOTE: For now a filterbackend is used.
# If it turns out, that the backend can not be easyly used,
# it might be a good idea to create own filters.
# def get_queryset(self):
#     queryset = Entry.objects.all()
#     cat = self.request.query_params.get("category")
#     if cat is not None:
#         queryset = queryset.filter(category=cat)
#     return queryset


class EntryDetails(generics.RetrieveAPIView):
    queryset = Entry.objects.all()  # type: ignore
    serializer_class = EntrySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]


class CategoryDetails(generics.RetrieveAPIView):
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["name"]
