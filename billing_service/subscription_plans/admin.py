from django.contrib import admin
from .models import SubscriptionPlan, BillingInfo, UserSubscription, TransactionHistory

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'max_streams']
    search_fields = ['name']
    list_filter = ['price']

class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'payment_reference']
    search_fields = ['user_id']
    list_filter = ['username']

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['billing_info', 'subscription_plan', 'start_date', 'end_date', 'status']
    search_fields = ['billing_info__username', 'subscription_plan__name']
    list_filter = ['status', 'subscription_plan']

class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['billing_info', 'amount', 'transaction_date', 'status']
    search_fields = ['billing_info__username']
    list_filter = ['status', 'transaction_date']

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(BillingInfo, BillingInfoAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
