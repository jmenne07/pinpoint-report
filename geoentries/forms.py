# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

from django.forms import ModelForm

from .models import Entry


class EntryForm(ModelForm):
    """
    Class, which handles the form-data in django
    """

    class Meta:
        model = Entry
        fields = [
            "title",
            "description",
            "latitude",
            "longitude",
            "category",
            "email",
            "image",
        ]
