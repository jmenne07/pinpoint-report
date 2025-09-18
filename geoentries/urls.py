# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns


from . import views


# TODO: Testing

urlpatterns = [
    path("", views.index, name="index"),
    path("requests/", views.EntryList.as_view()),
    path("request/<int:pk>", views.EntryDetails.as_view()),
    path("services/", views.CategoryList.as_view()),
    path("service/<int:pk>", views.CategoryDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)
