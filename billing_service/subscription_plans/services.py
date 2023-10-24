# services.py
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import SubscriptionPlan, BillingInfo, UserSubscription, TransactionHistory
import datetime

class SubscriptionService:

    @classmethod
    def list_plans(cls):
        return SubscriptionPlan.objects.all()

    @classmethod
    def subscribe(cls, username, user_id, plan_id):
        try:
            # Fetch or create BillingInfo
            billing_info, created = BillingInfo.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'username': username,
                    'payment_reference': 'Default_Payment_Reference'
                }
            )

            plan = SubscriptionPlan.objects.get(id=plan_id)
        except ObjectDoesNotExist:
            return False, "Plan or Billing Information not found"

        # Here you might want to call your Payment Gateway to actually charge the user.
        # For now, let's assume that the payment was successful.
        
        # Create a new transaction history
        TransactionHistory.objects.create(
            billing_info=billing_info,
            amount=plan.price,
            transaction_date=timezone.now().date(),
            status='Success'
        )

        # Create or update the User Subscription
        user_subscription, created = UserSubscription.objects.get_or_create(
            billing_info=billing_info,
            defaults={
                'subscription_plan': plan,
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + datetime.timedelta(days=plan.duration_days),
                'status': 'Active'
            }
        )
        
        if not created:
            user_subscription.subscription_plan = plan
            user_subscription.end_date = timezone.now().date() + datetime.timedelta(days=plan.duration_days)
            user_subscription.save()

        return True, "Successfully subscribed"


    @classmethod
    def get_user_subscriptions(cls, user_id):
        try:
            billing_info = BillingInfo.objects.get(user_id=user_id)
            user_subscriptions = billing_info.user_subscription.filter(status="Active")
            return user_subscriptions, None
        except ObjectDoesNotExist:
            return None, "Billing info does not exist for this user."
