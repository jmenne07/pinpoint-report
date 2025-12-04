# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from base64 import urlsafe_b64encode

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Entry, Mail

default_perms = [
    "view_category",
    "view_entry",
    "add_entry",
    "change_entry",
    "delete_entry",
    "view_entry",
]

mail_replacements = {
    "{{id}}": lambda entry: entry.id,
}


@receiver(post_save, sender=Group)
def add_default_group_permissions(sender, instance, created, **kwargs):
    if created:

        def add_permission_on_commit():
            perms = Permission.objects.filter(
                content_type__app_label="geoentries"
            ).filter(codename__in=default_perms)

            instance.permissions.add(*perms)
            print(perms)

        transaction.on_commit(add_permission_on_commit)


@receiver(post_save, sender=Entry)
def send_confirmation_mail_on_create(sender, instance, created, **kwargs):
    if created:
        send_external_mail("creation", instance)
        send_internal_mail("allocation", instance)


@receiver(pre_save, sender=Entry)
def presave_entry_handler(sender, instance, **kwargs):
    """
    Function receiving a pre_save signal when an entry is modified to send mails accordingly
    """
    try:
        old_entry = Entry.objects.get(pk=instance.id)
    except Entry.DoesNotExist:
        return

    def send_mails_on_commit():
        old_status = old_entry.status
        if old_status == 0 and instance.status == 1:
            send_close_link(instance)
            send_external_mail("info_allocation", instance)

        if instance.status == 2:
            send_external_mail("finished", instance)

        pass

    transaction.on_commit(send_mails_on_commit)


def send_external_mail(title: str, entry):
    send_entry_mail(title, entry, [entry.email])


def send_internal_mail(title, entry):
    mail_receiver = [entry.category.email]
    send_entry_mail(title, entry, mail_receiver)


def send_entry_mail(title: str, entry, mail_receiver):
    subject = ""
    message = ""
    mail_object = Mail.objects.get(title=title)
    if mail_object:
        subject = mail_object.subject
        message = mail_object.body
        for placeholder, func in mail_replacements.items():
            try:
                value = func(entry)
            except AttributeError:
                continue  # object does not have the attribute
            message = message.replace(placeholder, str(value))

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, mail_receiver)
    else:
        print("warning, mail not found")
        print("no mail will be sent")


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
        print("Warning")
        # WARNING: Error handling has to be improved
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ["test@pinpoint.de"])
    print(message)
