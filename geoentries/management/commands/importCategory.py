# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.
import json

from django.core.management.base import BaseCommand

from ...serializers import CategorySerializer


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        with open(path, "r") as f:
            data = json.load(f)
            for cat in data:
                ser = CategorySerializer(data=cat)
                if ser.is_valid():
                    ser.save()
                else:
                    print(ser.errors)
