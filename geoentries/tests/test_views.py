# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture(scope="module")
def index_url():
    return reverse("geoentries:index")


@pytest.fixture(scope="module")
def create_url():
    return reverse("geoentries:create")


class Test_Index:
    def test_index_view(self, client, index_url):
        response = client.get(index_url)
        print(index_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "geoentries/index.html")


class Test_EntryCreateView:
    @pytest.mark.django_db
    def test_create_view(self, client, create_url):
        response = client.get(create_url)
        assert response.status_code == 200
        assertTemplateUsed(response, "geoentries/create.html")

    def test_form_vlaid(self):
        # TODO: create this test
        pass
