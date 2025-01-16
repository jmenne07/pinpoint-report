from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published")

    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):  # type: ignore
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # type:ignore

    def __str__(self):  # type: ignore
        return self.choice_text
