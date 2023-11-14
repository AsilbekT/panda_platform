# Generated by Django 4.2.4 on 2023-11-14 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('video_app', '0035_subscriptionplan_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'unique_together': {('username', 'content_type', 'object_id')},
            },
        ),
    ]
