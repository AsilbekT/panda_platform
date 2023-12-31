# Generated by Django 4.2.5 on 2023-11-02 22:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0015_paymenttransaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenttransaction',
            name='transaction_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]
