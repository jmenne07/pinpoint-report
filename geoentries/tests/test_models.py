# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from geoentries.models import Category, Entry

# Test category models

# TODO: Test No circle


@pytest.mark.django_db
def test_create_category():
    cat1 = Category.objects.create(name="cat1", description="dies ist ein Test")
    cat2 = Category.objects.create(name="cat2", parent=cat1)

    assert cat1.name == "cat1"
    assert cat1.description == "dies ist ein Test"
    assert cat1.subcategories.first() == cat2
    assert cat2.parent == cat1
    assert cat2.name == "cat2"


def test_name_length():
    cat = Category()
    with pytest.raises(ValidationError, match="darf nicht leer sein."):
        cat.full_clean()
    cat.name = "A" * 101
    with pytest.raises(ValidationError, match="aus höchstens"):
        cat.full_clean()


@pytest.fixture
def cat():
    return Category.objects.create(name="cat1")


# test entry models
@pytest.mark.django_db
@pytest.mark.skip("Error has to be found ")
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

    assert str(entry) == f"#1: {cat.name} ({entry.title})"


def test_category_not_null():
    entry = Entry(title="Test", latitude=0, longitude=0)
    with pytest.raises(ValidationError, match="darf nicht null"):
        entry.full_clean()


def test_title_length():
    entry = Entry()
    with pytest.raises(ValidationError, match="darf nicht null"):
        entry.full_clean()
    entry.title = "A" * 101
    with pytest.raises(ValidationError, match="aus höchstens"):
        entry.full_clean()


@pytest.mark.django_db
def test_latitude_validators(cat):
    entry = Entry(title="Test", category=cat)
    entry.longitude = 0
    entry.latitude = -91

    with pytest.raises(ValidationError, match="größer oder gleich -90"):
        entry.full_clean()

    entry.latitude = 91
    with pytest.raises(ValidationError, match="kleiner oder gleich 90"):
        entry.full_clean()

    entry.latitude = 9.1234567890123450
    with pytest.raises(ValidationError, match="höchstens 6 Dezimalstellen"):
        entry.full_clean()


@pytest.mark.django_db
def test_longitude_validators(cat):
    entry = Entry(title="Test", category=cat)
    entry.longitude = -180.00001
    entry.latitude = 0

    with pytest.raises(ValidationError, match="größer oder gleich -180"):
        entry.full_clean()

    entry.longitude = 180.00001
    with pytest.raises(ValidationError, match="kleiner oder gleich 180"):
        entry.full_clean()

    entry.longitude = 10.123456789012345
    with pytest.raises(ValidationError, match="höchstens 6 Dezimalstellen"):
        entry.full_clean()
