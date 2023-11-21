from celery import shared_task
from .models import Review, UserActivity, UserWatchData
from datetime import timedelta
from django.utils import timezone
from django.db import models


@shared_task
def save_watch_data(user_id, content_id, watch_duration):
    # If watch_duration is greater than a certain threshold, you might consider the content as fully watched.
    # You need to know the total duration of the content to set this threshold accurately.
    # Example threshold in seconds (e.g., 1 hour)
    threshold_for_full_watch = 3600
    fully_watched = watch_duration >= threshold_for_full_watch

    obj, created = UserWatchData.objects.update_or_create(
        user_id=user_id,
        content_id=content_id,
        defaults={
            'watch_duration': models.F('watch_duration') + watch_duration,
            'fully_watched': fully_watched
        }
    )


@shared_task
def add_user_activity(user_id, content_id, activity_type, watch_timestamp):
    UserActivity.objects.update_or_create(
        user_id=user_id,
        content_id=content_id,
        defaults={
            'activity_type': activity_type,
            'timestamp': watch_timestamp
        }
    )


@shared_task
def add_review(user_id, content_id, review_text, rating):
    Review.objects.update_or_create(
        user_id=user_id,
        content_id=content_id,
        defaults={
            'review_text': review_text,
            'rating': rating
        }
    )
