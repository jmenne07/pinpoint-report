# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.forms import ModelForm, Form, CharField, ChoiceField
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
            "formated_adress",
        ]


class EntryFilterForm(Form):
    q = CharField(required=False, label="Search")
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(), level_indicator="--", required=False
    )

    # status = ChoiceField(choices=[("", "All")] + list(Entry.Status), required=False)
