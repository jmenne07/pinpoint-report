# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
"""
Module which contains classes reprensenting the database structure
of the project.
"""

# TODO: Testing

from base64 import urlsafe_b64encode
from typing import override

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    """
    A class defining a Category for the database.
    Groups define who can work on an entry.
    """

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    # TODO: Prevent circles
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
    )

    description = models.TextField(null=True, blank=True)

    #  users = models.ManyToManyField(User, related_name="owner", blank=True)
    #  groups = models.ManyToManyField(Group, related_name="group_owner", blank=True)

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

    class Meta:
        verbose_name_plural = "Entries"

    # id set automatically by django

    # Time based fields
    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=settings.DEBUG)

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

    @override
    def __str__(self) -> str:
        return str(self.title)

    def save(self, **kwargs) -> None:
        try:
            old_status = Entry.objects.get(pk=self.id).status
            if old_status == 0 and self.status == 1:
                send_close_link(self)
        except Entry.DoesNotExist:
            pass
        super().save(**kwargs)


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


def send_close_link(entry: Entry) -> None:
    """
    Sends a link, which sets the status of an entry from "In progress" to "Closed"
    """

    # TODO: Test
    if not settings.SEND_MAIL:
        # TODO: Probably should raise an Error, since to work emails have to be send
        return

    padded_id = str(entry.id).zfill(6)
    cipher = ChaCha20.new(key=settings.KEY)
    byte_text = bytes(padded_id, "utf-8")
    ciphertext = cipher.encrypt(byte_text)
    nonce = cipher.nonce

    b64nonce = urlsafe_b64encode(nonce).decode("utf-8")
    b64ct = urlsafe_b64encode(ciphertext).decode("utf-8")

    host = "localhost:8000"
    url = reverse("geoentries:index")
    link = f"{host}{url}{b64nonce}/{b64ct}"

    subject = "Close link"
    message = link

    mail_object = Mail.objects.filter(title="closelink").first()
    if mail_object:
        subject = mail_object.subject
        message = mail_object.body
        message = message.replace("{{id}}", str(entry.id))
        message = message.replace("{{link}}", link)

    else:
        print("Warngin")
        # WARNING: Error handling has to be improved
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["test@pinpoint.de"])
    print(message)
