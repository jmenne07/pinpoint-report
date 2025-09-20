# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.test import TestCase
import pytest
from .models import Entry, Category
from django.utils import timezone


# Test category models
@pytest.mark.django_db
def test_create_category():
    cat1 = Category.objects.create(name="cat1", description="dies ist ein Test")
    cat2 = Category.objects.create(name="cat2", parent=cat1)

    assert cat1.name == "cat1"
    assert cat1.description == "dies ist ein Test"
    assert cat1.subcategories.first() == cat2
    assert cat2.parent == cat1
    assert cat2.name == "cat2"


@pytest.fixture
def cat():
    return Category.objects.create(name="cat1")


@pytest.mark.django_db
def test_create_entry(cat):
    before = timezone.now()
    entry = Entry.objects.create(title="Test", category=cat, latitude=0, longitude=0)
    after = timezone.now()

    assert entry.title == "Test"
    assert entry.category == cat
    assert entry.latitude == 0
    assert entry.longitude == 0
    assert entry.status == 0

    assert before <= entry.creation_time <= after

    assert str(entry) == "Test"

    # TODO: Test Updated at
