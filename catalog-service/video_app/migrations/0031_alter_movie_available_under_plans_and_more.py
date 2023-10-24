# Generated by Django 4.2.4 on 2023-10-16 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0030_movie_slug_series_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='available_under_plans',
            field=models.ManyToManyField(blank=True, to='video_app.subscriptionplan'),
        ),
        migrations.AlterField(
            model_name='series',
            name='available_under_plans',
            field=models.ManyToManyField(blank=True, to='video_app.subscriptionplan'),
        ),
    ]
