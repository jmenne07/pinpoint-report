# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from django.contrib import admin, messages
from django.utils.translation import ngettext

# Register your models here.

from .models import Category, Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = None
    readonly_fields = ["creation_time", "last_change"]
    actions = ["make_public"]
    list_display = ["title", "category__name", "state", "published"]

    list_filter = ["state"]

    @admin.action(description="Publish selected reports.")
    def make_public(self, request, queryset):
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


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exlude = None
    inlines = [CategoryInline]
