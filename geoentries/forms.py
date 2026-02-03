# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.forms import ModelForm
from mptt.forms import TreeNodeChoiceField

from .models import Category, Entry


class EntryForm(ModelForm):
    """
    Class, which handles the form-data in django
    """

    category = TreeNodeChoiceField(
        queryset=Category.objects.all(), level_indicator="-- "
    )

    class Meta:
        model = Entry
        fields = [
            # "title",
            "description",
            "latitude",
            "longitude",
            "category",
            "email",
            "image",
        ]
