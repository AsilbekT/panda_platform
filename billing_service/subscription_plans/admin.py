from django.contrib import admin
from .models import PaymentTransaction, SubscriptionPlan, BillingInfo, UserSubscription, TransactionHistory


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days', 'max_streams']
    search_fields = ['name']
    list_filter = ['price']


class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'payment_reference']
    search_fields = ['user_id']
    list_filter = ['username']


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['billing_info', 'subscription_plan',
                    'start_date', 'end_date', 'status']
    search_fields = ['billing_info__username', 'subscription_plan__name']
    list_filter = ['status', 'subscription_plan']


class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['billing_info', 'amount', 'transaction_date', 'status']
    search_fields = ['billing_info__username']
    list_filter = ['status', 'transaction_date']


class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'amount', 'currency', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['user__username', 'click_trans_id',
                     'merchant_trans_id', 'merchant_prepare_id', 'merchant_confirm_id']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(BillingInfo, BillingInfoAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
