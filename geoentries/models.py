# Copyright 2026 Jörn Menne
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
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from datetime import timedelta

django_engine = engines["django"]
logger = logging.getLogger(__name__)
# Create your models here.


class Category(MPTTModel):
    """
    A class defining a Category for the database.
    Groups define who can work on an entry.

    """

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    class MPTTMeta:
        order_insertion_by = ["name"]

    name = models.CharField(max_length=100, unique=True, primary_key=True)
    # TODO: Prevent circles
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
        verbose_name=_("Parent"),
    )

    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

    email = models.EmailField(blank=True, null=True)
    extern = models.EmailField(blank=True, null=True, verbose_name=_("External-Mail"))
    monitoring_mail = models.EmailField(
        blank=True, null=True, verbose_name="Monitoring-Mail"
    )

    duration = models.DurationField(
        default=timedelta(weeks=4), verbose_name=_("duration")
    )

    @override
    def __str__(self) -> str:
        return str(self.name)


class Entry(models.Model):
    """
    A class representing the model of a service request
    """

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")

    class Status(models.IntegerChoices):
        """
        A class which defines the possible states of a request
        """

        OPEN = 0, _("open")
        IN_PROGRESS = 1, _("in progress")
        CLOSED = 2, _("closed")
        ARCHIVED = 3, _("archived")

    # id set automatically by django

    # Time based fields
    creation_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation-time")
    )
    update_time = models.DateTimeField(auto_now=True, verbose_name=_("Update-time"))
    done_date = models.DateField(blank=True, null=True, verbose_name=_("Done-date"))

    published = models.BooleanField(default=False, verbose_name=_("published"))

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name="entries",
        verbose_name=Category._meta.verbose_name,
    )

    status = models.IntegerField(choices=Status, default=0)  # type: ignore

    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))

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
    image = models.ImageField(
        blank=True, null=True, upload_to="images/", verbose_name=_("Image")
    )
    history = HistoricalRecords()

    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"))
    remark = models.TextField(null=True, blank=True, verbose_name=_("Remark"))

    send_closelink = models.BooleanField(
        default=False, verbose_name=_("Send closelink")
    )

    formated_adress = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name=_("Adress")
    )

    show_image = models.BooleanField(default=True, verbose_name=_("show_image"))

    @override
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.title is None or self.title == "":
            self.title = f"#{self.pk}-{self.category.name}"
            super().save(*args, **kwargs)

        if not self.done_date and self.category:
            self.done_date = self.update_time + self.category.duration
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

    class Meta:
        verbose_name = _("Groupprofile")
        verbose_name_plural = _("Groupprofiles")

    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, verbose_name=Group._meta.verbose_name
    )
    categories = models.ManyToManyField(
        Category, verbose_name=Category._meta.verbose_name_plural
    )

    def __str__(self) -> str:
        return "Categories"


class Condition(models.Model):
    LOOKUP_CHOICES = [
        ("exact", "Equals (==)"),
        ("iexact", "Equals (Case-Insensitive)"),
        ("contains", "Contains"),
        ("gt", "Greater Than (>)"),
        ("gte", "Greater Than or Equal (>=)"),
        ("lt", "Less Than (<)"),
        ("lte", "Less Than or Equal (<=)"),
        ("in", "Is in (comma-separated list)"),
    ]

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")

    name = models.CharField(max_length=50)
    field_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Fieldname")
    )

    lookup_type = models.CharField(
        max_length=32, choices=LOOKUP_CHOICES, default="exact"
    )
    # new value
    expected_value = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=_("Expected value")
    )

    previous_value = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Only needed for a transition change",
        verbose_name=_("Previous value"),
    )

    trigger_on_create = models.BooleanField(
        default=True, verbose_name=_("trigger on create")
    )
    trigger_on_update = models.BooleanField(
        default=True, verbose_name=_("trigger on update")
    )

    def __str__(self):
        return self.name


class MailTrigger(models.Model):
    class Meta:
        verbose_name = _("Email-Trigger")
        verbose_name_plural = _("Email-Triggers")

    event = models.CharField(max_length=128, unique=True)
    model_name = models.CharField(max_length=50, null=True, verbose_name="Modelname")

    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    conditions = models.ManyToManyField(
        Condition, verbose_name=Condition._meta.verbose_name_plural
    )

    def __str__(self):
        return f"Event: {self.event}"


class MailTemplate(models.Model):
    """
    Database entries for mails
    """

    class Meta:
        verbose_name = _("Email-Template")
        verbose_name_plural = _("EMail-Templates")

    MAIL_TYPE_CHOICES = [
        ("info", "info"),
        ("intern", "intern"),
        ("extern", "extern"),
    ]
    title = models.CharField(max_length=50, unique=True, verbose_name=_("Title"))
    subject = models.CharField(max_length=80, verbose_name=_("Subject"))
    body = models.TextField(blank=False, null=False, default="", verbose_name=_("body"))
    mail_type = models.CharField(
        max_length=32,
        choices=MAIL_TYPE_CHOICES,
        default="info",
        verbose_name=_("Mailtype"),
    )

    triggers = models.ManyToManyField(
        MailTrigger,
        related_name="mails",
        blank=True,
        verbose_name=_("template_triggers"),
    )

    @override
    def __str__(self):
        return self.title

    def render_and_send(self, context, receipient_list=None):
        if settings.SEND_MAIL:
            # TODO: Get receipient_list
            subject_template = django_engine.from_string(self.subject)
            message_template = django_engine.from_string(self.body)
            # WARNING: context explicitly calles Entry
            # TODO: Find a better solution
            if not receipient_list:
                receipient_list = []
                if self.mail_type == "info":
                    receipient_list.append(context["Entry"].email)
                if self.mail_type == "intern":
                    receipient_list.append(context["Entry"].category.email)
                if self.mail_type == "extern":
                    receipient_list.append(context["Entry"].category.extern)

                monitoring_mail = context["Entry"].category.monitoring_mail
                if monitoring_mail:
                    receipient_list.append(monitoring_mail)

            try:
                if self.title == "closelink":
                    context["link"] = context["Entry"].create_finish_link()
                subject = subject_template.render(context)
                message = message_template.render(context)

                send_mail(
                    subject, message, settings.DEFAULT_FROM_EMAIL, receipient_list
                )
            except Exception as e:
                logger.error(f"Could not send mail {self.title} because of error {e}")
