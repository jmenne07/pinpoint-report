# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing
from base64 import urlsafe_b64decode
from typing import Any

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, IntegerField, OuterRef, QuerySet, Subquery, Q
from django.db.models.functions import Coalesce
from django.http import HttpRequest, JsonResponse
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

from geoentries.forms import EntryFilterForm, EntryForm

from .models import Category, Entry
from .serializers import CategorySerializer, EntrySerializer


class IndexView(TemplateView):
    model = Entry
    template_name = "geoentries/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        entries = Entry.objects.filter(published=True)

        context["locations"] = entries
        context["entries"] = entries.order_by("-creation_time")[:2]
        return context


def get_location_data(request: HttpRequest):
    locations = Entry.objects.filter(published=True).values(
        "id", "latitude", "longitude"
    )
    return JsonResponse(list(locations), safe=False)


class EntryCreateView(CreateView):
    template_name = "geoentries/create.html"
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy("geoentries:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = context["form"]
        print("CATEGORY FIELD CLASS:", type(form.fields["category"]))
        print("CHOICES SAMPLE:", list(form.fields["category"].choices)[:5])

        return context


class EntryListView(ListView):
    template_name = "geoentries/list.html"
    context_object_name = "entries"
    model = Entry

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        form = EntryFilterForm(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data["q"]
            category = form.cleaned_data["category"]
            # status= form.cleaned_data["status"]
            status = False
            if q:
                queryset = queryset.objects.filter(
                    Q(title__icontains=q) | Q(description__icontains=q),
                )

                # Catfilter
            if category:
                queryset = queryset.filter(category=category)

            # statusfilter
            if status:
                queryset = queryset.filter(status=status)

        queryset = queryset.filter(published=True)
        return queryset

    def get_context_data(self, **kwargs: Any):
        contextdata = super().get_context_data(**kwargs)
        contextdata["filter_form"] = EntryFilterForm(self.request.GET)
        return contextdata


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

    # TODO: Check if the link is set correct


class CategoryAPIViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: Test
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, XMLRenderer]
    filterset_fields = ["name"]


class StatsView(ListView):
    model = Category
    template_name = "geoentries/stats.html"
    context_object_name = "categories"

    def get_queryset(self) -> QuerySet[Category]:
        subquery = (
            Entry.objects.filter(
                category__tree_id=OuterRef("tree_id"),
                category__lft__gte=OuterRef("lft"),
                category__rght__lte=OuterRef("rght"),
            )
            .values("category__tree_id")
            .annotate(count=Count("id"))
            .values("count")
        )
        return Category.objects.annotate(
            count=Coalesce(
                Subquery(subquery),
                0,
                output_field=IntegerField(),
            )
        ).order_by("tree_id", "lft")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status_counts = (
            Entry.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        status_map = dict(Entry.Status.choices)

        context["status_counts"] = [
            {"status": status_map[s["status"]], "count": s["count"]}
            for s in status_counts
        ]

        return context


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
