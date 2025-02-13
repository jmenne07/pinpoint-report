# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
from base64 import urlsafe_b64encode
from typing import override

from Crypto.Cipher import ChaCha20
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from georeport.models import Category, Image, Report

from .minio import get_url


# TODO: reorder


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    can_delete = False
    show_change_link = True

    @override
    def has_change_permission(self, request, obj=None):
        return False


class CategoryUserInline(admin.TabularInline):
    model = Category.users.through  # type:ignore through is not known
    extra = 0
    can_delete = False

    @override
    def has_change_permission(self, request, obj=None):
        return False


class CategoryGroupInline(admin.TabularInline):
    model = Category.groups.through  # type:ignore through is not known
    extra = 0
    can_delete = False

    @override
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Class extending model-Admin to register the model Category on
    the admin site, such that the model can be edited on there.
    """

    exclude = ["users", "groups"]
    inlines = [CategoryInline, CategoryGroupInline, CategoryUserInline]
    search_fields = ["name"]
    # TODO: Prevent circles while creating groups

    @override
    def has_change_permission(self, request, obj=None):
        """
        Override has change_permission, in order to only
        allow user associated to a category to modify the
        category.
        The association can be directly (user to category) or
        indirectly over groups.
        """
        user = request.user
        basepermission = super().has_change_permission(request, obj)
        # Always allow superusers to modify
        if user.is_superuser:
            return True

        if obj:
            allowed = getAllowedUsers(obj)
        else:
            allowed = []

        if basepermission and (request.user in allowed):
            return True
        return False


def getAllowedUsers(category):
    """
    Function to get a queryset with all users, which should
    have access to the category.

    Arguments:
        category: Category
            A category, to which allowed users shall be found

    Returns:
        Queryset containing all uses associated with the category.
    """
    # TODO: Find better location for this function
    qs = category.users.all()
    for group in category.groups.all():
        qs = qs | group.user_set.all()

    if category.parent:
        qs = qs | getAllowedUsers(category.parent)
    return qs


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    can_delete = True

    @override
    def has_change_permission(self, request, obj=None):
        return False

    def image_preview(self, obj):
        if obj.file:
            url = get_url(obj.file)
            return format_html(f'<img src="{url}" width="300px" height="300px"/>')
        return ""

    fields = ("image_preview",)
    readonly_fields = ("image_preview",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # TODO: If images are added through admin, they are not in minio. This feature has to be added
    exclude = [
        "_oldState",
    ]
    readonly_fields = ["created_at", "updated_at"]
    list_display = ["title", "category__name", "state", "published"]
    list_filter = ["state"]
    inlines = [ImageInline]

    @admin.action(description="Publish selected reports.")
    def make_public(self, request, queryset):
        """
        Admin-action to bulk-publish reports.

        Arguments:
            request: The current http-request. The request is created by performing the action.
            queryset: A queryset containing every Report, which was selected by the user.

        """
        updated = queryset.update(published=True)
        self.message_user(
            request,
            ngettext(
                "%d report was published",
                "%d reports were published",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @override
    def save_model(self, request, obj, form, change):
        """
        Override of the default save-function of a ModelAdmin to provide
        custom actions before the object is saved.

        For information about the arguments please refer to admin.ModelAdmin.save_model.
        """
        # send an update-mail if the state was chagned
        if not obj.state == obj._oldState:
            send_update(obj)

        # TODO: close__link shall also work on descendants
        if obj.state == 1 and obj.category.close_with_link:
            send_close_link(obj)

        obj._oldstate = obj.state
        super().save_model(request, obj, form, change)

    actions = [make_public]


def send_update(report):
    # TODO: Tests
    if not settings.SEND_MAIL:
        return
    recipient_list = [report.email]
    subject = f"Report with title {report.title} was updated."
    message = f"The state of the report {report.id}: {report.title} was changed to {report.state}."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True,
    )


def send_close_link(report):
    """
    If the category allows it, a link is send to the owners of the category,
    over which the category can be closed
    """
    # TODO: Tests

    if not settings.SEND_MAIL:
        return
    # Create a encrypted version of the id to send as a close_link
    message = ""
    padded_id = str(report.id).zfill(6)
    cipher = ChaCha20.new(key=settings.KEY)
    byte_text = bytes(padded_id, "utf-8")
    ciphertext = cipher.encrypt(byte_text)
    nonce = cipher.nonce

    b64nonce = urlsafe_b64encode(nonce).decode("utf-8")
    b64ct = urlsafe_b64encode(ciphertext).decode("utf-8")
    url = reverse("georeport:index")
    message = f"localhost:8000{url}{b64nonce}/{b64ct}"
    print(message)

    subject = f"Close link for report {report.id}"
    user = getAllowedUsers(report.category)
    recipient_list = []
    for u in user:
        recipient_list.append(u.email)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True,
    )


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    exlude = None
    inlines = [CategoryUserInline]


@admin.register(Group)
class MyGroupAdmin(GroupAdmin):
    exlude = None
    inlines = [CategoryGroupInline]
