# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
"""
Module which contains classes reprensenting the database structure
of the project.
"""

# TODO: Testing

import logging
from base64 import urlsafe_b64encode
from typing import override

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template import engines
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords

django_engine = engines["django"]
logger = logging.getLogger(__name__)
# Create your models here.


class Category(MPTTModel):
    """
    A class defining a Category for the database.
    Groups define who can work on an entry.
    """

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    # TODO: Prevent circles
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    description = models.TextField(null=True, blank=True)

    email = models.EmailField(blank=True, null=True)
    extern = models.EmailField(blank=True, null=True)
    monitoring_mail = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ["name"]

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

    class Meta:
        verbose_name_plural = "Entries"

    # id set automatically by django

    # Time based fields
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    done_date = models.DateField(blank=True, null=True)

    published = models.BooleanField(default=settings.AUTO_PUBLISH)

    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="entries"
    )

    status = models.IntegerField(choices=Status, default=0)  # type: ignore

    description = models.TextField(null=True, blank=True)

    # Location
    # TODO: Change to geodjango later on
    # NOTE: Latitude is between -90 and 90°, while Longitude is between -180 and 180°
    # Therefore the latitude field is slightly smaller
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        null=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )

    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    history = HistoricalRecords()

    notes = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)

    send_closelink = models.BooleanField(default=False)

    formated_adress = models.CharField(max_length=1000, blank=True, null=True)

    @override
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.title is None or self.title == "":
            self.title = f"#{self.pk}-{self.category.name}"
            super().save(*args, **kwargs)
        return

    @override
    def __str__(self) -> str:
        return (
            "#"
            + str(self.pk)
            + ": "
            + str(self.category)
            + " ("
            + str(self.title)
            + ")"
        )

    def create_finish_link(self):
        padded_id = str(self.id).zfill(6)
        cipher = ChaCha20.new(key=settings.KEY)
        byte_text = bytes(padded_id, "UTF-8")
        ciphertext = cipher.encrypt(byte_text)
        nonce = cipher.nonce

        b64nonce = urlsafe_b64encode(nonce).decode("utf-8")
        b64ct = urlsafe_b64encode(ciphertext).decode("utf-8")

        host = settings.HOST
        url = reverse("geoentries:index")
        link = f"{host}{url}{b64nonce}/{b64ct}"

        return link


class GroupProfile(models.Model):
    """
    A small model to expand the groups
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return "Categories"


class Mail(models.Model):
    """
    Database entries for mails
    """

    title = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=80)
    body = models.TextField(blank=False, null=False, default="")

    @override
    def __str__(self):
        return self.title

    def render_and_send(self, context, receipient_list):
        __import__("pdb").set_trace()
        subject_template = django_engine.from_string(self.subject)
        message_template = django_engine.from_string(self.body)

        try:
            subject = subject_template.render(context)
            message = message_template.render(context)

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, receipient_list)
        except Exception as e:
            logger.error(f"Could not send mail {self.title} because of error {e}")
