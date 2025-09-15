# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.db import models
from django.utils import choices

# Create your models here.


class ServiceRequest(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 1
        CLOSED = 2

    # id set automatically by django

    title = models.CharField(max_length=100)

    status = models.IntegerField(choices=Status, default=0)  # type: ignore

    description = models.TextField(null=True, blank=True)

    creation_time = models.DateTimeField(auto_now=True)
    updated_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
