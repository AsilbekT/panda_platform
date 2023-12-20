from django.db.models import Sum, Avg, Count
from django.views import View
from django.http import JsonResponse
from subscription_plans.models import PaymentTransaction
from .utils import standard_response
from rest_framework.views import APIView
from django.utils.timezone import now
import datetime


class TotalRevenueView(APIView):
    def get(self, request):
        today = now().date()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        total_revenue = PaymentTransaction.objects.filter(
            status='Completed').aggregate(total=Sum('amount'))['total']

        daily_revenue = PaymentTransaction.objects.filter(
            status='Completed', completed_at__date=today).aggregate(total=Sum('amount'))['total']

        weekly_revenue = PaymentTransaction.objects.filter(
            status='Completed', completed_at__date__gte=start_of_week).aggregate(total=Sum('amount'))['total']

        monthly_revenue = PaymentTransaction.objects.filter(
            status='Completed', completed_at__date__gte=start_of_month).aggregate(total=Sum('amount'))['total']

        data = {
            'total_revenue': total_revenue,
            'daily_revenue': daily_revenue,
            'weekly_revenue': weekly_revenue,
            'monthly_revenue': monthly_revenue
        }
        return standard_response(True, 'Revenue data retrieved', data)


class RevenueByPlanView(APIView):
    def get(self, request):
        revenue_by_plan = PaymentTransaction.objects.values('plan__name').annotate(
            total_revenue=Sum('amount'),
            transaction_count=Count('id'),
            average_revenue_per_plan=Avg('amount')
        )
        return standard_response(True, 'Revenue by Plan retrieved', {'revenue_by_plan': list(revenue_by_plan)})


class AverageRevenuePerUserView(APIView):
    def get(self, request):
        arpu_data = PaymentTransaction.objects.values('user__username').annotate(
            total_revenue=Sum('amount'),
            average_revenue=Avg('amount'),
            transaction_count=Count('id')
        )
        return standard_response(True, 'Average Revenue per User retrieved', {'arpu': list(arpu_data)})


class TransactionSuccessFailureRateView(APIView):
    def get(self, request):
        total_transactions = PaymentTransaction.objects.count()
        status_counts = PaymentTransaction.objects.values(
            'status').annotate(count=Count('id'))
        success_rate = next((item['count'] for item in status_counts if item['status']
                            == 'Completed'), 0) / total_transactions * 100
        failure_rate = 100 - success_rate
        return standard_response(True, 'Transaction Rate retrieved', {'success_rate': success_rate, 'failure_rate': failure_rate, 'status_counts': list(status_counts)})
