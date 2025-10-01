# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

# TODO: More tests for the api


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_category_list(client):
    url = reverse("geoentries:category-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_entry_list(client):
    url = reverse("geoentries:entry-list")
    response = client.get(url)
    assert response.status_code == 200
