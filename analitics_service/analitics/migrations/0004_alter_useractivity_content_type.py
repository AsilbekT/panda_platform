# Generated by Django 4.2.7 on 2023-12-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analitics', '0003_useractivity_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='content_type',
            field=models.CharField(choices=[('movie', 'MOVIE'), ('series', 'SERIES')], max_length=100),
        ),
    ]
