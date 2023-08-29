from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, 
    DirectorViewSet, 
    MovieViewSet, 
    SeriesViewSet, 
    EpisodeViewSet
    )

router = DefaultRouter()

router.register(r'genres', GenreViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'series', SeriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('series/<int:series_id>/episodes/', EpisodeViewSet.as_view({'get': 'list'}), name='series-episodes'),
]
