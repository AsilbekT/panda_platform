# admin.py

from django.contrib import admin
from .models import UserActivity, Review, UserWatchData


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'content_id', 'activity_type', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user_id', 'content_id')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'content_id', 'rating', 'timestamp')
    list_filter = ('rating', 'timestamp')
    search_fields = ('user_id', 'content_id')


@admin.register(UserWatchData)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'content_id', 'watch_duration', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user_id', 'content_id')
