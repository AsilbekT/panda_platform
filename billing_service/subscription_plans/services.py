# services.py
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import SubscriptionPlan, BillingInfo, UserSubscription, TransactionHistory
import datetime
from django.db import transaction


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
            user_subscription.end_date = timezone.now().date(
            ) + datetime.timedelta(days=plan.duration_days)
            user_subscription.save()

        return True, "Successfully subscribed"

    @classmethod
    def create_transaction(cls, billing_info, plan, amount, transaction_id):
        transaction_date = timezone.now().date()
        print(billing_info, plan, amount, transaction_id)
        TransactionHistory.objects.create(
            billing_info=billing_info,
            amount=amount,
            transaction_date=transaction_date,
            status='Success',  # Or other status based on the payment response
            transaction_id=transaction_id
        )

    @classmethod
    def create_subscription(cls, billing_info, plan):
        start_date = timezone.now().date()
        end_date = start_date + datetime.timedelta(days=plan.duration_days)
        subscription, created = UserSubscription.objects.update_or_create(
            billing_info=billing_info,
            defaults={
                'subscription_plan': plan,
                'start_date': start_date,
                'end_date': end_date,
                'status': 'Active'
            }
        )
        return subscription

    @classmethod
    def get_user_subscriptions(cls, username):
        try:
            billing_info = BillingInfo.objects.get(username=username)
            user_subscriptions = billing_info.user_subscription.filter(
                status="Active")
            return user_subscriptions, None
        except ObjectDoesNotExist:
            return None, "Billing info does not exist for this user."

    @classmethod
    def process_payment(cls, billing_info_id, plan_id, amount, transaction_id):
        try:
            billing_info = BillingInfo.objects.get(pk=billing_info_id)
            plan = SubscriptionPlan.objects.get(pk=plan_id)
        except (BillingInfo.DoesNotExist, SubscriptionPlan.DoesNotExist) as e:
            return False, str(e)
        # Assume that payment is done here and we get a response
        transaction = cls.create_transaction(
            billing_info, plan, amount, transaction_id)

        subscription = cls.create_subscription(billing_info, plan)
        return True, "Subscription and transaction created successfully."
