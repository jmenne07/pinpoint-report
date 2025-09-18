# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
"""
Module which contains classes reprensenting the database structure
of the project.
"""

from typing import override
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Category(models.Model):
    """
    A class defining a Category for the database.
    Groups define who can work on an entry.
    """

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    description = models.TextField(null=True, blank=True)

    users = models.ManyToManyField(User, related_name="owner", blank=True)
    groups = models.ManyToManyField(Group, related_name="group_owner", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    @override
    def __str__(self) -> str:
        return str(self.name)


class Entry(models.Model):
    """
    A class representing the model of a service request
    """

    class Status(models.IntegerChoices):
        """
        A class which defines the possible states of a request
        """

        OPEN = 0
        IN_PROGRESS = 1
        CLOSED = 2
        ARCHIVED = 3

    # id set automatically by django

    # Time based fields
    creation_time = models.DateTimeField(auto_now=True)
    updated_datetime = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="entries"
    )

    status = models.IntegerField(choices=Status, default=0)  # type: ignore

    description = models.TextField(null=True, blank=True)

    # Location
    # NOTE: Latitude is between -90 and 90°, while Longitude is between -180 and 180°
    # Therefore the latitude field is slightly smaller
    # TODO: Restrict geocoordinates to the values above (or even smaller)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    @override
    def __str__(self) -> str:
        return str(self.title)
