# Generated by Django 3.0.8 on 2020-09-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_auto_20200905_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='image',
            field=models.CharField(default='article_images/1.jpg', max_length=200),
            preserve_default=False,
        ),
    ]
