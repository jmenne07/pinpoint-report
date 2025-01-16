from django.contrib import admin

# Register your models here.

from .models import *


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInLine]

    list_display = ["question_text", "pub_date", "was_published_recently"]
    search_fields = ["question_text"]


admin.site.register(Choice)
