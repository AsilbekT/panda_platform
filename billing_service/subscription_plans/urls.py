from django.urls import path
from . import views


urlpatterns = [
    path('plans/', views.SubscriptionPlanListView.as_view(), name='list-plans'),
    path('payment-url/', views.PaymentUrlView.as_view(), name='create-payment-url'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('<str:username>/subscriptions/',
         views.UserSubscriptionView.as_view(), name='subscriptions'),
]
