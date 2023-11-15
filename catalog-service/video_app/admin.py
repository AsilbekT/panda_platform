from django.contrib import admin
from .models import Banner, Comment, FavoriteContent, Season, UserSubscription
from django.utils.html import format_html
from django.contrib import admin, messages
from .models import (
    Genre,
    Director,
    Movie,
    Series,
    Episode,
    Banner,
    Catagory,
    VideoConversionType,
    SubscriptionPlan
)


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_days']
    search_fields = ['name']
    list_filter = ['price']


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# class SubscriptionPlanInline(admin.TabularInline):
#     model = SubscriptionPlan
#     extra = 1


class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'is_ready',
                    'is_premiere', 'has_trailer')
    search_fields = ('title', 'release_date')
    list_filter = ('is_ready', 'is_premiere', 'has_trailer')
    ordering = ('release_date',)

    def save_model(self, request, obj, form, change):
        if obj.is_free and obj.available_under_plans.exists():
            messages.set_level(request, messages.ERROR)
            messages.error(
                request, "Free content should not have any associated subscription plans.")
        else:
            super().save_model(request, obj, form, change)


class MovieAdmin(ContentAdmin):
    list_display = ContentAdmin.list_display + \
        ('is_featured', 'is_trending', 'production_cost', 'licensing_cost')
    list_filter = ContentAdmin.list_filter + ('is_featured', 'is_trending')


class SeriesAdmin(ContentAdmin):
    list_display = ContentAdmin.list_display + \
        ('number_of_seasons', 'is_featured', 'is_trending')
    list_filter = ContentAdmin.list_filter + \
        ('number_of_seasons', 'is_featured', 'is_trending')


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('series', 'season', 'episode_number',
                    'title', 'duration_minute')
    search_fields = ('series__title', 'title')
    list_filter = ('series', 'season')
    ordering = ('series', 'season', 'episode_number')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_object', 'status', 'priority',
                    'created_at', 'updated_at')
    list_filter = ('status',  'created_at')
    search_fields = ('name', 'content_object__title')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('content_type')
        return queryset


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('series', 'season_number', 'trailer_url')
    search_fields = ('series__title', 'trailer_url')
    list_filter = ('series',)


class FavoriteContentAdmin(admin.ModelAdmin):
    list_display = ('username', 'content_object_display')

    def content_object_display(self, obj):
        return obj.content_object
    content_object_display.short_description = 'Content'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'content', 'created_at',
                    'updated_at', 'is_reply')
    list_filter = ('created_at', 'username')
    search_fields = ('username', 'content')
    raw_id_fields = ('parent',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('parent')


# Register your models here.
admin.site.register(Comment, CommentAdmin)
admin.site.register(FavoriteContent, FavoriteContentAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Catagory)
admin.site.register(VideoConversionType)
admin.site.register(UserSubscription)
