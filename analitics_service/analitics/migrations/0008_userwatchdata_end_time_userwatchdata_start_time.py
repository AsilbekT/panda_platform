# Generated by Django 4.2.7 on 2023-11-21 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analitics', '0007_alter_useractivity_device_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwatchdata',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userwatchdata',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
