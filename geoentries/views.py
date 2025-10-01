# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing
from django.views.generic import FormView, TemplateView, CreateView
from rest_framework import mixins, viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from .models import Category, Entry
from .serializers import CategorySerializer, EntrySerializer


class IndexView(TemplateView):
    template_name = "geoentries/index.html"


class EntryCreateView(CreateView):
    template_name = "geoentries/create.html"
    model = Entry
    fields = ["title", "description", "latitude", "longitude", "category"]


class ListView(TemplateView):
    template_name = "geoentries/list.html"


class EntryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Entry.objects.all()  # type: ignore
    serializer_class = EntrySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["id", "category", "status"]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    enderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["name"]
