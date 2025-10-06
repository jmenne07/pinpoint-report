# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing
from base64 import urlsafe_b64decode

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, ListView, TemplateView
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
    fields = ["category", "title", "description", "latitude", "longitude", "email"]
    success_url = reverse_lazy("geoentries:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        # TODO: Test
        send_mail("TEst", "test", settings.DEFAULT_FROM_EMAIL, [self.object.email])  # type: ignore
        return response


class EntryListView(ListView):
    template_name = "geoentries/list.html"
    context_object_name = "entries"
    model = Entry


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


@require_GET
def close_with_link_view(request, b64nonce, b64ct):
    # TODO: Test
    """
    A view which acceprts an nonce and a ciphertext.
    The nonce and ciphertext are then decrypted to a report.
    If this report is in the correct state, the report will change its state to closed.

    Args:
        request: The http-request
        b64nonce: A base64 encoded nonce
        b64ct: A base64 encoded ciphertext
    """
    nonce = urlsafe_b64decode(b64nonce)
    ct = urlsafe_b64decode(b64ct)
    cipher = ChaCha20.new(key=settings.KEY, nonce=nonce)
    pk = cipher.decrypt(ct)
    id = int(pk)
    entry = get_object_or_404(Entry, pk=id)

    if entry.status == 1:
        entry.status = 2
        entry.save()
    return redirect("geoentries:index")
