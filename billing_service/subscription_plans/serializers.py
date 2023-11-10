from rest_framework import serializers
from .models import UserSubscription, SubscriptionPlan


# Serializer for SubscriptionPlan model
class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price', 'duration_days']

# Serializer for UserSubscription model


class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription_plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = ['id', 'subscription_plan',
                  'start_date', 'end_date', 'status']
