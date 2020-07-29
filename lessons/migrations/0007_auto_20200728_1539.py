# Generated by Django 3.0.8 on 2020-07-28 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0006_auto_20200728_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='posted_by',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='posted_by_id',
            new_name='posted_by',
        ),
    ]
