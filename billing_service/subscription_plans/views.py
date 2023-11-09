from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import json
import uuid
from django.http import QueryDict

from subscription_plans.utils import generate_merchant_confirm_id, generate_merchant_prepare_id
from .models import BillingInfo, PaymentTransaction, SubscriptionPlan, TransactionHistory, UserSubscription
from .services import SubscriptionService
from .decorators import verify_token
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from .utils import create_click_payment_url


CLICK_PAYMENT_URL = "https://my.click.uz/services/pay"
CLICK_MERCHANT_SERVICE_ID = "30124"
CLICK_MERCHANT_ID = "22603"
# The URL where Click will send the user after payment
CLICK_RETURN_URL = "http://localhost:8080/"


@method_decorator(csrf_exempt, name='dispatch')
class SubscriptionPlanListView(View):
    def get(self, request):
        # Fetch all subscription plans and serialize them
        plans = SubscriptionPlan.objects.all()
        plan_data = [{"id": plan.id, "name": plan.name,
                      "price": str(plan.price)} for plan in plans]
        return JsonResponse(plan_data, safe=False)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        plan_id = data.get('plan_id')

        try:
            plan = SubscriptionPlan.objects.get(pk=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return JsonResponse({"error": "Plan does not exist"}, status=400)

        user_billing, created = BillingInfo.objects.get_or_create(
            user_id=user_id,
            defaults={
                'payment_reference': 'Default_Payment_Reference'
            }
        )
        transaction_id = str(uuid.uuid4())

        transaction = PaymentTransaction.objects.create(
            user=user_billing,
            plan=plan,
            status='Initiated',
            amount=plan.price,
            transaction_id=transaction_id
        )

        payment_url = create_click_payment_url(
            user_id, transaction.id, plan.price)
        payment_url += f"{transaction.id}"
        return JsonResponse({"paymentUrl": payment_url})


@method_decorator([csrf_exempt, verify_token], name='dispatch')
class SubscribeView(View):
    @transaction.atomic
    def post(self, request):
        user_id = request.POST.get('user_id')
        plan_id = request.POST.get('plan_id')
        username = request.username
        if not all([user_id, plan_id]):
            return JsonResponse({"message": "Missing required fields."}, status=400)

        success, message = SubscriptionService.subscribe(
            username, user_id, plan_id)
        if success:
            return JsonResponse({"message": "Successfully subscribed"})
        else:
            return JsonResponse({"message": message}, status=400)

# class UpdateBillingInfoView(View):
#     def put(self, request):
#         user_id = request.PUT.get('user_id')
#         payment_reference = request.PUT.get('payment_reference')

#         success = BillingService.update_billing_info(user_id, payment_reference)
#         if success:
#             return JsonResponse({"message": "Billing info updated successfully"}, status=200)
#         else:
#             return JsonResponse({"message": "Failed to update billing info"}, status=400)


# # Update Subscription View
# @method_decorator([verify_token], name='dispatch')
# class UpdateSubscriptionView(View):
#     def post(self, request):
#         user_id = request.POST.get('user_id')
#         new_plan_id = request.POST.get('new_plan_id')

#         # Fetch the existing user subscription and the new plan
#         user_subscription = UserSubscription.objects.filter(billing_info__user_id=user_id).first()
#         new_plan = SubscriptionPlan.objects.get(id=new_plan_id)

#         if user_subscription is None:
#             return JsonResponse({"message": "No existing subscription found for this user."}, status=400)

#         # Your existing logic for updating subscription
#         user_subscription.subscription_plan = new_plan
#         user_subscription.save()

#         return JsonResponse({"message": "Successfully updated subscription plan"})


@method_decorator([csrf_exempt, verify_token], name='dispatch')
class UserSubscriptionView(View):
    def get(self, request, username):
        try:
            user_subscriptions, error_message = SubscriptionService.get_user_subscriptions(
                username)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if error_message:
            return JsonResponse({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        if user_subscriptions and user_subscriptions.exists():
            serializer = UserSubscriptionSerializer(
                user_subscriptions, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse({"message": "No subscriptions found for this user"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator([csrf_exempt], name='dispatch')
class PrepareClickPaymentView(View):
    @transaction.atomic
    def post(self, request):
        try:
            query_dict = QueryDict(request.body.decode('utf-8'))
            click_trans_id = query_dict.get('click_trans_id')
            merchant_trans_id = query_dict.get('merchant_trans_id')
            amount = query_dict.get('amount')

            payment_transaction = PaymentTransaction.objects.get(
                id=merchant_trans_id
            )

            if payment_transaction.status not in ['Initiated', 'Prepared']:
                return JsonResponse({
                    'error': 1,
                    'error_note': 'Invalid transaction status'
                }, status=400)

            merchant_prepare_id = generate_merchant_prepare_id()

            payment_transaction.merchant_prepare_id = merchant_prepare_id
            payment_transaction.status = 'Prepared'
            payment_transaction.save()

            return JsonResponse({
                'click_trans_id': click_trans_id,
                'merchant_trans_id': merchant_trans_id,
                'merchant_prepare_id': merchant_prepare_id,
                'error': 0,
                'error_note': 'Success'
            })

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({
                'error': 1,
                'error_note': 'Transaction not found or amount mismatch'
            }, status=400)
        except Exception as e:
            # Proper error logging should be here
            return JsonResponse({
                'error': 1,
                'error_note': f'An error occurred: {str(e)}'
            }, status=400)


@method_decorator([csrf_exempt], name='dispatch')
class CompleteClickPaymentView(View):
    @transaction.atomic
    def post(self, request):
        try:
            payment_data = QueryDict(request.body.decode('utf-8'))
            click_trans_id = payment_data.get('click_trans_id')
            merchant_trans_id = payment_data.get('merchant_trans_id')
            amount = payment_data.get('amount')
            merchant_confirm_id = generate_merchant_confirm_id()

            if not all([click_trans_id, merchant_trans_id, amount]):
                return JsonResponse({'error': 1, 'message': 'Missing required parameters'}, status=400)

            payment_transaction = PaymentTransaction.objects.get(
                id=merchant_trans_id)

            billing_info_id = payment_transaction.user_id
            plan_id = payment_transaction.plan_id

            success, message = SubscriptionService.process_payment(
                billing_info_id, plan_id, amount, payment_transaction.id)
            if success:

                payment_transaction.status = 'Completed'
                payment_transaction.completed_at = timezone.now()
                payment_transaction.merchant_confirm_id = merchant_confirm_id
                payment_transaction.save()
                billing_info = payment_transaction.user
                subscription_plan = payment_transaction.plan

                # Calculate subscription dates
                today = timezone.now().date()
                start_date = today
                # Assuming duration is in days
                end_date = today + \
                    timedelta(days=subscription_plan.duration_days)

                # Create or update the UserSubscription
                user_subscription, created = UserSubscription.objects.update_or_create(
                    billing_info=billing_info,
                    defaults={
                        'subscription_plan': subscription_plan,
                        'start_date': start_date,
                        'end_date': end_date,
                        'status': 'Active'  # or any other logic to determine status
                    }
                )

                return JsonResponse({
                    'click_trans_id': click_trans_id,
                    'merchant_trans_id': merchant_trans_id,
                    'merchant_confirm_id': merchant_confirm_id,
                    'error': 0,
                    'error_note': 'Payment processed and subscription activated'
                })
            else:
                return JsonResponse({'error': 1, 'error_note': message}, status=400)

        except PaymentTransaction.DoesNotExist:
            return JsonResponse({'error': 1, 'message': 'Transaction not found'}, status=400)
        except Exception as e:
            # Log the exception here
            return JsonResponse({'error': 1, 'error_note': f'An error occurred: {str(e)}'}, status=400)
