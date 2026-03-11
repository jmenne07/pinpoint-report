# Copyright 2026 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


from django.forms import CharField, ChoiceField, Form, ModelForm, TextInput
from mptt.forms import TreeNodeChoiceField

from .models import Category, Entry


class EntryForm(ModelForm):
    """
    Class, which handles the form-data in django
    """

    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        level_indicator="-- ",
        empty_label="Bitte auswählen.",
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
    q = CharField(
        required=False,
        label="Search",
        widget=TextInput(attrs={"placeholder": "Volltextsuche hier eingeben"}),
    )
    category = TreeNodeChoiceField(
        queryset=Category.objects.all(),
        level_indicator="--",
        required=False,
        empty_label="Kategorie-Filter",
    )

    status = ChoiceField(
        choices=[("", "Alle Status")] + Entry.Status.choices, required=False
    )
