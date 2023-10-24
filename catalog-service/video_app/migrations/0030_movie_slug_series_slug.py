# Generated by Django 4.2.4 on 2023-10-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0029_rename_subscription_plan_movie_available_under_plans_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='series',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
