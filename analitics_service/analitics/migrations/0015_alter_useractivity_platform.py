# Generated by Django 4.2.7 on 2023-11-21 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analitics', '0014_useractivity_platform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='platform',
            field=models.CharField(max_length=100),
        ),
    ]
