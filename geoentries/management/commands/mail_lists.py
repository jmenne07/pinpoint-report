# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.urls import reverse

from ...models import Category


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
