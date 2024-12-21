from asyncio import wait
from django.db import models

from django.forms import ModelForm
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

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

    # TODO add status
    #
    def __str__(self):
        return self.title


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "description", "latitude", "longitude", "category"]
