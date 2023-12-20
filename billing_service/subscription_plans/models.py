from datetime import timedelta
import uuid
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from .utils import send_request_to_catalog_service, send_user_subscription_to_catalog
from django.db.models.signals import post_save
from django.db.models.signals import post_save, post_delete

# SubscriptionPlan model


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    max_streams = models.IntegerField()

    def __str__(self):
        return self.name

# BillingInfo model


class BillingInfo(models.Model):
    # Unique identifier from User service
    user_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=200, unique=True)
    # Reference ID or token from third-party payment service
    payment_reference = models.CharField(max_length=100)

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

    billing_info = models.ForeignKey(
        BillingInfo, on_delete=models.CASCADE, related_name="user_subscription")
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    grace_period_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.billing_info.username}'s Subscription to {self.subscription_plan.name}"

# TransactionHistory model


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('Prepared', 'Prepared'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
        ('Initiated', 'Initiated')
    ]

    user = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    click_trans_id = models.CharField(max_length=255)
    merchant_trans_id = models.CharField(max_length=255)
    merchant_prepare_id = models.CharField(
        max_length=255, null=True, blank=True)
    merchant_confirm_id = models.CharField(
        max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='UZS')
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_data = models.JSONField(null=True, blank=True)
    payment_type = models.CharField(max_length=50, null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)
    refund_status = models.BooleanField(default=False)
    prepared_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Payment Transaction on {self.created_at}"

    def process_payment(self):
        # Use the payment type to delegate to the correct handler
        if self.payment_type == 'click':
            return self._process_click_payment()
        elif self.payment_type == 'paypal':
            return self._process_paypal_payment()

    def _process_click_payment(self):
        # Logic specific to processing Click payments
        pass

    def _process_paypal_payment(self):
        # Logic specific to processing PayPal payments
        pass


class TransactionHistory(models.Model):
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.ForeignKey(
        PaymentTransaction, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failure', 'Failure'),
    ]
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Success')

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


@receiver(post_save, sender=UserSubscription)
def post_save_send_to_catalog(sender, instance, **kwargs):
    """
    Signal handler for when a UserSubscription instance is saved or updated.
    """
    send_user_subscription_to_catalog(instance)
