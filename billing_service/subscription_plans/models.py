from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from .utils import send_request_to_catalog_service
from django.db.models.signals import post_save
from django.db.models.signals import post_save, post_delete

# SubscriptionPlan model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_streams = models.IntegerField()

    def __str__(self):
        return self.name

# BillingInfo model
class BillingInfo(models.Model):
    user_id = models.CharField(max_length=50, unique=True)  # Unique identifier from User service
    username = models.CharField(max_length=200, unique=True)
    payment_reference = models.CharField(max_length=100)  # Reference ID or token from third-party payment service

    def __str__(self):
        return f"{self.username}'s Billing Info"

# UserSubscription model
class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Paused', 'Paused'),
        ('Exhausted', 'Exhausted'),
        ('Expired', 'Expired'),
    ]
    
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE, related_name="user_subscription")
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    grace_period_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.billing_info.username}'s Subscription to {self.subscription_plan.name}"

# TransactionHistory model
class TransactionHistory(models.Model):
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failure', 'Failure'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Success')

    def __str__(self):
        return f"{self.billing_info.username}'s Transaction on {self.transaction_date}"



@receiver(post_save, sender=SubscriptionPlan)
def model_saved_or_updated(sender, instance, created, **kwargs):
    """
    Signal handler for when a SubscriptionPlan instance is saved or updated.
    """
    if created:
        send_request_to_catalog_service(instance, 'POST')
    else:
        send_request_to_catalog_service(instance, 'PUT')


@receiver(post_delete, sender=SubscriptionPlan)
def model_deleted(sender, instance, **kwargs):
    """
    Signal handler for when a SubscriptionPlan instance is deleted.
    """
    send_request_to_catalog_service(instance, 'DELETE')
