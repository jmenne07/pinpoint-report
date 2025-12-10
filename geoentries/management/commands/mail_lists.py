# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from ...models import Entry, Category
from ...signals import send_internal_mail
from django.urls import reverse
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cats = Category.objects.all()
        for cat in cats:
            send_list(cat)


def send_list(cat):
    message = """
        Hallo, 
            hier sind alle offenen Anliegen der Kategory {cat}:
        """

    for entry in cat.entries.all():
        message += (
            "- "
            + entry.title
            + ": "
            + reverse("admin:geoentries_entry_change", args=[entry.pk])
        )

    send_mail("Offene Anliegen", message, settings.DEFAULT_FROM_EMAIL, [cat.email])
