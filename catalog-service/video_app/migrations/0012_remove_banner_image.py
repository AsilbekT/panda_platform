# Generated by Django 4.2.4 on 2023-09-07 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0011_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='image',
        ),
    ]