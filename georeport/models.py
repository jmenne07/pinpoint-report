# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
"""
Module which contains classes representing the database structure
of the project.
"""

from django.db import models
from django.contrib.auth.models import Group, User
from typing import override

from django.forms import DecimalField

# Create your models here.


class Category(models.Model):
    """
    A class representing a Category in the database.
    """

    # TODO: Prevent circles
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    user = models.ManyToManyField(User, related_name="owner", blank=True)
    groups = models.ManyToManyField(Group, related_name="group_owner", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    @override
    def __str__(self) -> str:
        return str(self.name)


class Report(models.Model):
    """
    A class representing a Report in the database.
    """

    class State(models.IntegerChoices):
        """
        A small class, which provide the possible states of a report
        """

        NEW = 0
        IN_PROGESS = 1
        FINISHED = 2
        ARCHIVE = 3

    # Timebased autofields
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # Fields to be filled at creation time
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="reports"
    )
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    # TODO: Images

    # Fields set at creation
    state = models.IntegerField(choices=State, default=0)  # type: ignore Correct type can not be dtermined
    _oldState = models.IntegerField(choices=State, default=0)  # type: ignore Correct type can not be dtermined

    """
        The old statevariable is neede to determine, if the state was changed.
    """
    published = models.BooleanField(default=False)  # type: ignore Correct type can not be dtermined

    # Location
    # NOTE: Latitude is between -90 and 90°, while Longitude is between -180 and 180°
    # Therefore the latitude field is slightly smaller
    # TODO: Restrict geocoordinates to the values above (or even smaller)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)

    @override
    def __str__(self) -> str:
        return str(self.title)


# TODO: Image
