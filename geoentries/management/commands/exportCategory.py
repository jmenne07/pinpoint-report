import json

from django.core.management.base import BaseCommand

from ...models import Category
from ...serializers import CategorySerializer


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("path", type=str)

    def handle(self, *args, **kwargs):
        cats = Category.objects.all()
        ser = CategorySerializer(cats, many=True)

        path = kwargs["path"]
        with open(path, "w") as f:
            f.write(json.dumps(ser.data, indent=4))
