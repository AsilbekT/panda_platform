# Generated by Django 4.2.4 on 2023-11-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_app', '0031_alter_movie_available_under_plans_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50, unique=True)),
                ('username', models.CharField(max_length=200, unique=True)),
                ('subscription_plan_name', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Paused', 'Paused'), ('Exhausted', 'Exhausted'), ('Expired', 'Expired')], default='Active', max_length=50)),
            ],
        ),
    ]
