# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from ...serializers import UserSerializer


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        ser = UserSerializer(users, many=True)

        path = kwargs["path"]
        with open(path, "w") as f:
            f.write(json.dumps(ser.data, indent=4))
