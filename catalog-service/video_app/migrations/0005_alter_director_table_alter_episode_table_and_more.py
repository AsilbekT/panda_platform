# Generated by Django 4.2.4 on 2023-09-02 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0004_remove_series_main_content_url'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='director',
            table='director_table',
        ),
        migrations.AlterModelTable(
            name='episode',
            table='episode_table',
        ),
        migrations.AlterModelTable(
            name='genre',
            table='genre_table',
        ),
        migrations.AlterModelTable(
            name='movie',
            table='movie_table',
        ),
        migrations.AlterModelTable(
            name='series',
            table='series_table',
        ),
    ]