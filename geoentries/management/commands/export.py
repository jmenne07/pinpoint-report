# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import json

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from ...models import Category, GroupProfile, Mail
from ...serializers import (
    CategorySerializer,
    GroupProfileSerializer,
    GroupSerializer,
    MailSerializer,
    UserSerializer,
)


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("path", type=str)
        parser.add_argument("--add-entry", action="store_true", default=False)

    def handle(self, *args, **kwargs) -> None:
        path = kwargs["path"]

        groups = Group.objects.all()
        groupser = GroupSerializer(groups, many=True)

        groupProfiles = GroupProfile.objects.all()
        gpser = GroupProfileSerializer(groupProfiles, many=True)

        users = User.objects.all()
        userser = UserSerializer(users, many=True)

        cats = Category.objects.all()
        catser = CategorySerializer(cats, many=True)

        mails = Mail.objects.all()
        mailser = MailSerializer(mails, many=True)

        data = {}
        data["group"] = groupser.data
        data["user"] = userser.data
        data["cat"] = catser.data
        data["gps"] = gpser.data
        data["mail"] = mailser.data

        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4))
