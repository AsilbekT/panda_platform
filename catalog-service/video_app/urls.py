from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet,
    DirectorViewSet,
    MovieViewSet,
    SeriesViewSet,
    EpisodeViewSet,
    HomeAPIView,
    BannerViewSet
)

router = DefaultRouter()

router.register(r'genres', GenreViewSet, basename="genres")
router.register(r'directors', DirectorViewSet, basename="directors")
router.register(r'movies', MovieViewSet, basename="movies")
router.register(r'series', SeriesViewSet, basename="series")
router.register(r'banners', BannerViewSet, basename='banners')


urlpatterns = [
    path('', include(router.urls)),
    path('homeapi/', HomeAPIView.as_view(), name='home-api-view'),
    path('series/<int:series_id>/episodes/',
         EpisodeViewSet.as_view({'get': 'list'}), name='series-episodes'),
]
