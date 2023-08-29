# Generated by Django 4.2.4 on 2023-08-29 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_episode_movie_series_delete_content_episode_series'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='movie_earnings',
            new_name='licensing_cost',
        ),
        migrations.AddField(
            model_name='movie',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='is_trending',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movie',
            name='production_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='series',
            name='is_trending',
            field=models.BooleanField(default=False),
        ),
    ]
