# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture(scope="module")
def url():
    return reverse("geoentries:index")


class Test_Index:
    def test_view(self, client, url):
        response = client.get(url)
        print(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "geoentries/index.html")
