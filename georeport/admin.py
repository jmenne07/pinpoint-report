# Copyright: (c) 2025, Jörn Menne <jmenne@posteo.de>
# GNU General Public License v3.0 (see LICSENE or https://www.gnu.org/license/gpl-3.0.md)


from django.contrib import admin

# Register your models here.

from .models import Category, Report

admin.site.register(Report)
admin.site.register(Category)
