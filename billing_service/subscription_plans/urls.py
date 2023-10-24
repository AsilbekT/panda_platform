from django.urls import path
from . import views


urlpatterns = [
    path('plans/', views.SubscriptionPlanListView.as_view(), name='list-plans'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('<int:user_id>/subscriptions/', views.UserSubscriptionView.as_view(), name='subscriptions'),
]