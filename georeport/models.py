from django.db import models

from django.forms import ModelForm
# Create your models here.


class Report(models.Model):
    title = models.CharField(max_length=80)
    creation_time = models.DateTimeField(auto_now_add=True)
    # TODO last change shall be set to creation_time at creation_time
    last_change = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, null=True)

    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # TODO add status
    #
    def __str__(self):
        return self.title


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "description", "latitude", "longitude"]
