# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing
from base64 import urlsafe_b64decode
from typing import Any

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from rest_framework import mixins, viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_xml.renderers import XMLRenderer

from geoentries.forms import EntryForm

from .models import Category, Entry, Mail
from .serializers import CategorySerializer, EntrySerializer


class IndexView(TemplateView):
    model = Entry
    template_name = "geoentries/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["locations"] = Entry.objects.all()
        context["entries"] = Entry.objects.order_by("-creation_time")[:2]
        return context


def get_location_data(request: HttpRequest):
    locations = Entry.objects.all().values("id", "latitude", "longitude")
    return JsonResponse(list(locations), safe=False)


class EntryCreateView(CreateView):
    template_name = "geoentries/create.html"
    model = Entry
    fields = [
        "category",
        "title",
        "description",
        "latitude",
        "longitude",
        "email",
        "image",
    ]
    success_url = reverse_lazy("geoentries:index")

    def form_valid(self, form: EntryForm):
        response = super().form_valid(form)
        # TODO: Test
        subject = "Confirmation"
        message = f"Das Anliegen wurde mit der ID {self.object.id} erstellt."

        mail_object = Mail.objects.filter(title="creation").first()
        if mail_object:
            subject = mail_object.subject
            message = mail_object.body.replace("{{id}}", str(self.object.id))
        else:
            print("warning, mail not found")
        # WARNING: Error handling has to be improved
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.object.email],  # type: ignore
        )
        return response


class EntryListView(ListView):
    template_name = "geoentries/list.html"
    context_object_name = "entries"
    model = Entry

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        queryset = queryset.filter(published=True)
        return queryset


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "geoentries/update.html"
    model = Entry
    fields = [
        "category",
        "status",
        "published",
        "title",
        "description",
        "latitude",
        "longitude",
        "email",
        "image",
    ]

    success_url = reverse_lazy("geoentries:index")


class EntryDetailView(DetailView):
    model = Entry
    template_name = "geoentries/detail.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        if request.user.is_authenticated:
            return redirect("geoentries:update", pk=self.object.pk)
        return super().get(request, *args, **kwargs)


class EntryAPIViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    # TODO: Test
    queryset = Entry.objects.all()  # type: ignore
    serializer_class = EntrySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["id", "category", "status"]


class CategoryAPIViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: Test
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    enderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["name"]


@require_GET
def close_with_link_view(request: HttpRequest, b64nonce: str, b64ct: str):  # type: ignore
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
