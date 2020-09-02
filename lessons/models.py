from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    topic = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    video_link = models.CharField(max_length=200)
    image_link = models.CharField(max_length=200)
    date_pub = models.DateTimeField('Date Published')
    syllabus = models.CharField(max_length=200)
    is_open = models.BooleanField()

    def __str__(self):
        return self.topic


class AdditionalMaterialsLessons(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.CharField(max_length=400)


class Comment(models.Model):
    topic = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text


class Articles(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=1000)
    desc = models.TextField()
    author = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
