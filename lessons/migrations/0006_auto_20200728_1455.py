# Generated by Django 3.0.8 on 2020-07-28 09:55

from django.db import migrations


def populate_author(apps, schema_editor):
    Comment = apps.get_model('lessons', 'Comment')
    User = apps.get_model('auth', 'User')
    for comment in Comment.objects.all():
        if not comment.posted_by:
            comment.posted_by_id_id = 1

        else:
            user = User.objects.get(username=comment.posted_by)
            comment.posted_by_id = user

        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_comment_posted_by_id'),
    ]

    operations = [
        migrations.RunPython(populate_author)
    ]
