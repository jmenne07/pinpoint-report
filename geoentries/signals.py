# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


import logging

from django.conf import settings
from django.contrib.auth.models import Group, Permission, User
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Entry, MailTemplate, MailTrigger

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


@receiver(pre_save, sender=Entry)
def capture_old_instance(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            instance._old_instance = None
    else:
        instance._old_instance = None


@receiver(post_save, sender=Entry)
def evalute_mail_trigger(sender, instance, created, **kwargs):
    __import__("pdb").set_trace()
    model_name = sender.__name__
    active_triggers = MailTrigger.objects.filter(
        model_name=model_name, is_active=True
    ).prefetch_related("conditions")

    for trigger in active_triggers:
        all_met = True
        for condition in trigger.conditions.all():
            if created and not condition.trigger_on_create:
                all_met = False
                break
            if not created and not condition.trigger_on_update:
                all_met = False
                break

            if condition.field_name:
                look_up = f"{condition.field_name}__{condition.lookup_type}"
                matches = sender.objects.filter(
                    id=instance.id, **{look_up: condition.expected_value}
                ).exists()

                if not matches:
                    all_met = False
                    break

            if not created and condition.previous_value:
                old_instance = getattr(instance, "_old_instance", None)
                if old_instance:
                    old_value = str(getattr(old_instance, condition.field_name))
                    if old_value != condition.previous_value:
                        all_met = False
                        break
                else:
                    all_met = False
                    break

        if all_met:
            for template in trigger.mails.all():
                context = {f"{model_name}": instance}
                if template.title == "closelink":
                    if not context["Entry"].send_closelink:
                        break
                template.render_and_send(context)


def send_close_link(entry: Entry) -> None:
    """
    Sends a link, which sets the status of an entry from "In progress" to "Closed"
    """

    # TODO: Test
    if not settings.SEND_MAIL:
        # TODO: Probably should raise an Error, since to work emails have to be send
        return

    receipient = []
    receipient.append(entry.category.extern)

    mail_object = MailTemplate.objects.filter(title="closelink").first()
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
