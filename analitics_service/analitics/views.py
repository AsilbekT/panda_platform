from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserWatchDataSerializer, UserActivitySerializer, ReviewSerializer
from .tasks import save_watch_data, add_user_activity, add_review
from django.db.models import Avg, Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ContentRevenue, Review, UserActivity, UserWatchData


@api_view(['POST'])
def user_watch_data_view(request):
    if request.method == 'POST':
        serializer = UserWatchDataSerializer(data=request.data)
        if serializer.is_valid():
            save_watch_data.delay(**serializer.validated_data)
            return Response({'status': 'success', 'message': 'User watch data is being processed'})
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def user_activity_view(request):
    if request.method == 'POST':
        serializer = UserActivitySerializer(data=request.data)
        if serializer.is_valid():
            add_user_activity.delay(**serializer.validated_data)
            return Response({'status': 'success', 'message': 'User activity is being processed'})
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def review_view(request):
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            add_review.delay(**serializer.validated_data)
            return Response({'status': 'success', 'message': 'Review is being processed'})
        return Response(serializer.errors, status=400)

# For calculating the average watch duration of content


class TotalWatchDurationView(APIView):
    def get(self, request, content_id):
        total_duration = UserWatchData.objects.filter(content_id=content_id).aggregate(
            total_watch_duration=Sum('watch_duration'),
            watch_count=Count('id')
        )
        return Response(total_duration)


# For calculating the average rating of content


class TotalReviewsView(APIView):
    def get(self, request, content_id):
        reviews_stats = Review.objects.filter(content_id=content_id).aggregate(
            total_reviews=Count('id'),
            avg_rating=Avg('rating')
        )
        return Response(reviews_stats)


# For calculating the total revenue by content


class TotalRevenueView(APIView):
    def get(self, request):
        revenue_stats = ContentRevenue.objects.all().aggregate(
            total_revenue=Sum('revenue')
        )
        return Response(revenue_stats)


class UserTotalWatchStatisticsView(APIView):
    def get(self, request, user_id):
        total_watch_data = UserWatchData.objects.filter(user_id=user_id).aggregate(
            total_views=Count('id'),
            total_watch_time=Sum('watch_duration')
        )
        return Response(total_watch_data)


class ContentWatchCountView(APIView):
    def get(self, request, content_id):
        watch_counts = UserWatchData.objects.filter(
            content_id=content_id,
            fully_watched=True
        ).count()
        return Response({'watch_count': watch_counts})


class LastWatchedPositionView(APIView):
    def get(self, request, user_id, content_id):
        last_activity = UserActivity.objects.filter(
            user_id=user_id,
            content_id=content_id
        ).order_by('-timestamp').first()
        if last_activity:
            response_data = {
                'last_watched': last_activity.timestamp,
                'activity_type': last_activity.activity_type
            }
        else:
            response_data = {'message': 'No activity found.'}
        return Response(response_data)
