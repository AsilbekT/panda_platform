from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (FavoriteContentViewSet, VideoConversionTypeViewSet, GenreViewSet,
                    DirectorViewSet, MovieViewSet, SeriesViewSet, SeasonViewSet, EpisodeViewSet, BannerViewSet, CommentViewSet)

router = DefaultRouter()
router.register(r'favorite-contents', FavoriteContentViewSet)
router.register(r'video-conversion-types', VideoConversionTypeViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'episodes', EpisodeViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include("catalog_management_app.auth.urls")),
    path('', include(router.urls)),
]
