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

from .models import BillingInfo, SubscriptionPlan, TransactionHistory, UserSubscription
from .services import SubscriptionService
from .decorators import verify_token
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from django.views.decorators.csrf import csrf_exempt

class SubscriptionPlanListView(APIView):
    def get(self, request):
        plans = SubscriptionService.list_plans()
        plan_data = [{"id": plan.id, "name": plan.name, "price": str(plan.price)} for plan in plans]
        return JsonResponse(plan_data, safe=False)


@method_decorator([csrf_exempt, verify_token], name='dispatch')
class SubscribeView(View):
    @transaction.atomic
    def post(self, request):
        user_id = request.POST.get('user_id')
        plan_id = request.POST.get('plan_id')
        username = request.username
        if not all([user_id, plan_id]):
            return JsonResponse({"message": "Missing required fields."}, status=400)
        
        success, message = SubscriptionService.subscribe(username, user_id, plan_id)
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
    def get(self, request, user_id):
        try:
            user_subscriptions, error_message = SubscriptionService.get_user_subscriptions(user_id)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


        if error_message:
            return JsonResponse({"message": error_message}, status=status.HTTP_404_NOT_FOUND)

        if user_subscriptions and user_subscriptions.exists():
            serializer = UserSubscriptionSerializer(user_subscriptions, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

        return JsonResponse({"message": "No subscriptions found for this user"}, status=status.HTTP_404_NOT_FOUND)
