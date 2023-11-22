from django.urls import path
from .views import (TotalRevenueView, RevenueByPlanView,
                    AverageRevenuePerUserView, TransactionSuccessFailureRateView)

urlpatterns = [
    path('total-revenue/', TotalRevenueView.as_view(), name='total_revenue'),
    path('revenue-by-plan/', RevenueByPlanView.as_view(), name='revenue_by_plan'),
    path('arpu/', AverageRevenuePerUserView.as_view(), name='arpu'),
    path('transaction-rates/', TransactionSuccessFailureRateView.as_view(),
         name='transaction_rates'),
]
