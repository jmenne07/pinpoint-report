# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing

from django.contrib.auth.models import Group, User
from rest_framework import serializers

from geoentries.models import (
    Category,
    Condition,
    Entry,
    GroupProfile,
    MailTemplate,
    MailTrigger,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description", "parent"]


class EntrySerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(source="latitude")
    long = serializers.FloatField(source="longitude")

    class Meta:
        model = Entry
        fields = ["id", "title", "category", "status", "description", "long", "lat"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = []


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = []


class MailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTemplate
        exclude = []


class MailTriggerSerialier(serializers.ModelSerializer):
    class Meta:
        model = MailTrigger
        exclude = []


class ConditionSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        exclude = []


class GroupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProfile
        exclude = []
