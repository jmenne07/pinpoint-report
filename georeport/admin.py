# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)
from django.contrib import admin
from typing import override

from georeport.models import Category, Report


# TODO: CategoryAdmin


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    can_delete = False
    show_change_link = True

    @override
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Class extending model-Admin to register the model Category on
    the admin site, such that the model can be edited on there.
    """

    exclude = ["user", "groups"]
    inlines = [CategoryInline]
    search_fields = ["name"]
    # TODO: Prevent circles while creating groups


# TODO: ReportAdmin
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = [
        "_oldstate",
    ]
