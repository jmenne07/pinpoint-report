# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


import logging

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Entry, Mail

logger = logging.getLogger(__name__)

default_perms = [
    "view_category",
    "view_entry",
    "add_entry",
    "change_entry",
    "delete_entry",
    "view_entry",
]


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


@receiver(post_save, sender=User)
def add_staff_status(sender, instance, created, **kwargs):
    """
    Modifies the users, such that the staff-status is default
    """
    if created:

        def default_staff_status():
            instance.is_staff = True
            instance.save()

        transaction.on_commit(default_staff_status)


@receiver(post_save, sender=Entry)
def send_confirmation_mail_on_create(sender, instance, created, **kwargs):
    if created and settings.SEND_MAIL:
        __import__("pdb").set_trace()
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
        if not settings.SEND_MAIL:
            pass
        if old_entry.status == 0 and instance.status == 1:
            if instance.send_closelink and instance.category.extern:
                send_close_link(instance)
            send_external_mail("info_allocation", instance)

        if old_entry.category != instance.category:
            send_internal_mail("allocation", instance)
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
    mail_object = Mail.objects.get(title=title)
    context = {"entry": entry, "anliegen": entry}
    if mail_object:
        mail_object.render_and_send(context, mail_receiver)
    else:
        logger.warning(f"Mail with title {title} not found\nNo Mail will be send")


def send_close_link(entry: Entry) -> None:
    """
    Sends a link, which sets the status of an entry from "In progress" to "Closed"
    """

    __import__("pdb").set_trace()
    # TODO: Test
    if not settings.SEND_MAIL:
        # TODO: Probably should raise an Error, since to work emails have to be send
        return

    receipient = []
    receipient.append(entry.category.extern)

    mail_object = Mail.objects.filter(title="closelink").first()
    if mail_object:
        link = entry.create_finish_link()
        context = {"entry": entry, "anliegen": entry, "link": link}
        mail_object.render_and_send(context, receipient)

    else:
        print("Warning")
        # WARNING: Error handling has to be improved
    # TODO: Get Mail-receiver from category
    logger.info("Mail with closelink sent")
    # print(message)
