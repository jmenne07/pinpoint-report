# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("requests/", views.ServiceRequestList.as_view()),
]
