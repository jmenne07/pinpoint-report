# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.db.models import signals
from django.dispatch import receiver

default_perms = [
    "view_category",
    "view_entry",
    "add_entry",
    "change_entry",
    "delete_entry",
    "view_entry",
]


@receiver(signals.post_save, sender=Group)
def add_default_group_permissions(sender, instance, created, **kwargs):
    if created:

        def add_permission_on_commit():
            perms = Permission.objects.filter(
                content_type__app_label="geoentries"
            ).filter(codename__in=default_perms)
            __import__("pdb").set_trace()

            instance.permissions.add(*perms)
            print(perms)

        transaction.on_commit(add_permission_on_commit)
