# Generated by Django 4.2.4 on 2023-09-10 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0023_alter_episode_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='is_movie',
            field=models.BooleanField(default=True),
        ),
    ]