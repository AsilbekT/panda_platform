from rest_framework import serializers
from .models import UserWatchData, UserActivity, Review


class UserWatchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchData
        fields = ['user_id', 'content_id', 'watch_duration']


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['user_id', 'content_id', 'activity_type']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user_id', 'content_id', 'review_text', 'rating']
