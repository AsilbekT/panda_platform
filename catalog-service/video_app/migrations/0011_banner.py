# Generated by Django 4.2.4 on 2023-09-07 20:39

from django.db import migrations, models
import django.db.models.deletion
import video_app.utils


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('video_app', '0010_alter_movie_thumbnail_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='banner_images/', validators=[video_app.utils.validate_file_size, video_app.utils.validate_image_file])),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('priority', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'video_app'), ('model', 'movie')), models.Q(('app_label', 'video_app'), ('model', 'series')), _connector='OR'), null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
            options={
                'db_table': 'banner_table',
                'ordering': ['-priority', '-created_at'],
            },
        ),
    ]
