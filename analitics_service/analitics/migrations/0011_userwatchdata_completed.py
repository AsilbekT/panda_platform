# Generated by Django 4.2.7 on 2023-11-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analitics', '0010_userwatchdata_fast_forward_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwatchdata',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
