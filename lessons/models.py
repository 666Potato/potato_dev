import datetime

from django.db import models
from django.utils import timezone


class Lesson(models.Model):
    topic = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    video_link = models.CharField(max_length=200)
    date_pub = models.DateTimeField('Date Published')

    def __str__(self):
        return self.topic

    def published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_pub <= now


class Comment(models.Model):
    topic = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    posted_by = models.CharField(max_length=200)

    def __str__(self):
        return self.comment_text
