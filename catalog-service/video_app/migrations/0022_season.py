# Generated by Django 4.2.4 on 2023-09-09 23:37

from django.db import migrations, models
import django.db.models.deletion
import video_app.utils


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0021_movie_is_free_series_is_free'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.IntegerField()),
                ('trailer_url', models.URLField(blank=True, null=True)),
                ('thumbnail_image', models.ImageField(blank=True, null=True, upload_to='season_thumbnail_image/', validators=[video_app.utils.validate_file_size, video_app.utils.validate_image_file])),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='video_app.series')),
            ],
            options={
                'db_table': 'season_table',
                'unique_together': {('series', 'season_number')},
            },
        ),
    ]
