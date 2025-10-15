# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# TODO: Testing


app_name = "geoentries"

router = DefaultRouter()
router.register(r"requests", views.EntryAPIViewSet, basename="entry")
router.register(r"services", views.CategoryAPIViewSet, basename="category")


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create", views.EntryCreateView.as_view(), name="create"),
    path("entries", views.EntryListView.as_view(), name="list"),
    path("entry/<int:pk>", views.EntryDetailView.as_view(), name="detail"),
    path("update/<int:pk>", views.EntryUpdateView.as_view(), name="update"),
    path("open311/v2/", include(router.urls)),
    path("<str:b64nonce>/<str:b64ct>", views.close_with_link_view, name="finish"),
]
