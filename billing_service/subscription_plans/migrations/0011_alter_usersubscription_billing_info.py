# Generated by Django 4.2.5 on 2023-10-16 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0010_alter_usersubscription_billing_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='billing_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription', to='subscription_plans.billinginfo'),
        ),
    ]
