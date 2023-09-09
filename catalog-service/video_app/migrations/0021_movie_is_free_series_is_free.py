# Generated by Django 4.2.4 on 2023-09-09 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0020_movie_conversion_type_series_conversion_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='series',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
