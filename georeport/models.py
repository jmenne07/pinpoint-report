# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from asyncio import wait
from django.db import models
from django.contrib.auth.models import Group, User, Permission

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )

    group = models.ManyToManyField(User, related_name="owner")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


def get_default_related():
    def get_default_related():
        return Category.objects.first().id


class Report(models.Model):
    class State(models.IntegerChoices):
        NEW = 0
        FINISHED = 1

    title = models.CharField(max_length=80)
    creation_time = models.DateTimeField(auto_now_add=True)
    # TODO last change shall be set to creation_time at creation_time
    last_change = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    state = models.IntegerField(choices=State, default=0)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, default=get_default_related
    )

    published = models.BooleanField(default=True)

    email = models.EmailField()

    # TODO add status
    #
    def __str__(self):
        return self.title
