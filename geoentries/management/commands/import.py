# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import json

from django.core.management.base import BaseCommand

from ...serializers import (
    CategorySerializer,
    ConditionSerizalizer,
    EntrySerializer,
    GroupProfileSerializer,
    GroupSerializer,
    MailTemplateSerializer,
    MailTriggerSerialier,
    UserSerializer,
)

SERIALIZER_MAPPING = {
    "group": GroupSerializer,
    "user": UserSerializer,
    "cat": CategorySerializer,
    "gps": GroupProfileSerializer,
    "conds": ConditionSerizalizer,
    "trigger": MailTriggerSerialier,
    "mail": MailTemplateSerializer,
    "entry": EntrySerializer,
}


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs) -> None:
        path = kwargs["path"]
        with open(path, "r") as f:
            data = json.load(f)

            for key in data:
                ser_class = SERIALIZER_MAPPING.get(key)
                if not ser_class:
                    continue

                for x in data[key]:
                    ser = ser_class(data=x)
                    if ser.is_valid():
                        ser.save()
                    else:
                        print(ser.errors)
