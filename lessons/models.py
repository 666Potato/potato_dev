from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    topic = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    video_link = models.CharField(max_length=200)
    image_link = models.ImageField(verbose_name='Upload image', upload_to='lessons/images')
    date_pub = models.DateTimeField('Date Published')
    syllabus = models.CharField(max_length=200, default='Lesson syllabus')
    description = models.TextField(default='Lesson description goes here')
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.topic


class AdditionalMaterialLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField()
    link = models.TextField(null=True, blank=True)
    image = models.ImageField(verbose_name='Upload image', upload_to='lessons/images')


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
    image = models.ImageField(verbose_name='Upload image', upload_to='articles/images')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date_added',)
