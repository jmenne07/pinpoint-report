# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.


# TODO: Testing

from rest_framework import serializers

from geoentries.models import Category, Entry


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "parent"]


class EntrySerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(source="latitude")
    long = serializers.FloatField(source="longitude")

    class Meta:
        model = Entry
        fields = ["id", "title", "category", "status", "description", "long", "lat"]
