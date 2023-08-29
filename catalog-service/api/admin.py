from django.contrib import admin
from .models import Genre, Director, Movie, Series, Episode, Content

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'is_ready', 'is_premiere', 'has_trailer')
    search_fields = ('title', 'release_date')
    list_filter = ('is_ready', 'is_premiere', 'has_trailer')
    ordering = ('release_date',)

class MovieAdmin(ContentAdmin):
    list_display = ContentAdmin.list_display + ('is_featured', 'is_trending', 'production_cost', 'licensing_cost')
    list_filter = ContentAdmin.list_filter + ('is_featured', 'is_trending')

class SeriesAdmin(ContentAdmin):
    list_display = ContentAdmin.list_display + ('number_of_seasons', 'is_featured', 'is_trending')
    list_filter = ContentAdmin.list_filter + ('number_of_seasons', 'is_featured', 'is_trending')

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('series', 'season', 'episode_number', 'title', 'duration_minute')
    search_fields = ('series__title', 'title')
    list_filter = ('series', 'season')
    ordering = ('series', 'season', 'episode_number')

admin.site.register(Genre, GenreAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Episode, EpisodeAdmin)
