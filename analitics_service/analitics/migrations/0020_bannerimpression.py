# Generated by Django 4.2.7 on 2023-11-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analitics', '0019_bannerclick'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerImpression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_id', models.IntegerField()),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]