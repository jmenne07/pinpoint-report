# Copyright 2025 Jörn Menne
# Licensed under the Apache License, Version 2.0
# See NOTICE file for details.

# TODO: Testing

from base64 import urlsafe_b64encode

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib import admin
from django.urls import reverse

from .models import Category, Entry

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exlude = None


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    exlude = None


def send_close_link(entry) -> None:
    """
    Sends a link, which sets the status of an entry from "In progress" to "Closed"
    """

    # TODO: Test
    if not settings.SEND_MAIL:
        # TODO: Probably should raise an Error, since to work emails have to be send
        return

    padded_id = str(entry.id).zfill(6)
    cipher = ChaCha20.new(key=settings.KEY)
    byte_text = bytes(padded_id, "utf-8")
    ciphertext = cipher.encrypt(byte_text)
    nonce = cipher.nonce

    b64nonce = urlsafe_b64encode(nonce).decode("utf-8")
    b64ct = urlsafe_b64encode(ciphertext).decode("utf-8")

    host = "localhost:8000"
    url = reverse("geoentries:index")
    message = f"{host}{url}{b64nonce}/{b64ct}"
    print(message)
