# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.urls import base, path, include

from rest_framework.urlpatterns import format_suffix_patterns


from . import views


# TODO: Testing

from rest_framework.routers import DefaultRouter

app_name = "geoentries"

router = DefaultRouter()
router.register(r"requests", views.EntryViewSet, basename="entry")
router.register(r"services", views.CategoryViewSet, basename="category")


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create", views.EntryCreateView.as_view(), name="create"),
    path("entries", views.EntryListView.as_view(), name="list"),
    path("open311/v2/", include(router.urls)),
    path("<str:b64nonce>/<str:b64ct>", views.close_with_link_view, name="finish"),
]
