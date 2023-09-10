from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    GenreViewSet,
    DirectorViewSet,
    MovieViewSet,
    SeriesViewSet,
    SeasonViewSet,  # make sure to create this ViewSet
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

series_router = routers.NestedDefaultRouter(router, r'series', lookup='series')
# series/{series_id}/seasons/
series_router.register(r'seasons', SeasonViewSet, basename='series-seasons')

seasons_router = routers.NestedDefaultRouter(
    series_router, r'seasons', lookup='season')

# series/{series_id}/seasons/{season_id}/episodes/
seasons_router.register(r'episodes', EpisodeViewSet,
                        basename='seasons-episodes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(series_router.urls)),
    path('', include(seasons_router.urls)),
    path('homeapi/', HomeAPIView.as_view(), name='home-api-view'),
]
