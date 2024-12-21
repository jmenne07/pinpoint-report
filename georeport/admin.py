from django.contrib import admin

# Register your models here.

from .models import Category, Report

admin.site.register(Report)
admin.site.register(Category)
