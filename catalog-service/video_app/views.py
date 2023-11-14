from django.contrib.contenttypes.models import ContentType
from video_app.utils import decode_token, standardResponse, user_has_active_plan
from .models import Catagory, FavoriteContent, Genre, Director, Movie, Season, Series, Episode, Banner, SubscriptionPlan, UserSubscription, ContentType
from .serializers import (
    CategorySerializer,
    EpisodeSerializerDetails,
    GenreSerializer,
    DirectorSerializer,
    HomeMovieSerializer,
    MovieDetailSerializer,
    MovieSerializer,
    SeasonSerializer,
    SeasonWithEpisodesSerializer,
    SeriesDetailSerializer,
    SeriesListSerializer,
    SeriesSerializer,
    EpisodeSerializer,
    BannerSerializer,
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer
)
from .base_view import BaseViewSet
from video_app.utils import paginate_queryset
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DirectorViewSet(BaseViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(BaseViewSet):
    queryset = Movie.objects.all().order_by('id')
    # check_user_subscriptions()

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    def list(self, request, *args, **kwargs):
        genre_from_param = self.request.query_params.get('genre', None)
        queryset = self.queryset.filter(
            genre_id=genre_from_param) if genre_from_param else self.queryset

        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Movies retrieved", data=serializer.data, pagination=pagination_data)


class SeriesViewSet(BaseViewSet):
    serializer_class = SeriesSerializer

    def get_queryset(self):
        queryset = Series.objects.all().order_by('id')
        genre_from_param = self.request.query_params.get('genre', None)
        if genre_from_param:
            queryset = queryset.filter(genre_id=genre_from_param)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return SeriesListSerializer  # For listing series with only necessary fields
        elif self.action == 'retrieve':
            return SeriesDetailSerializer  # For detailed view of a single series
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Series retrieved", data=serializer.data, pagination=pagination_data)


class EpisodeViewSet(BaseViewSet):
    queryset = Episode.objects.all().order_by('series', 'season', 'episode_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return EpisodeSerializer
        elif self.action == 'retrieve':
            return EpisodeSerializerDetails
        return EpisodeSerializer

    def list(self, request, series_id=None, *args, **kwargs):
        queryset = self.queryset.filter(
            series_id=series_id) if series_id else self.queryset

        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = EpisodeSerializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Episodes retrieved", data=serializer.data, pagination=pagination_data)


class SeasonViewSet(BaseViewSet):
    queryset = Season.objects.all().order_by('season_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return SeasonSerializer
        elif self.action == 'retrieve':
            return SeasonWithEpisodesSerializer
        return SeasonSerializer


class CategoryViewSet(BaseViewSet):
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        try:
            categories = Catagory.objects.all()
            category_serializer = CategorySerializer(
                categories, many=True, context={'request': request})

            # Aggregate data
            data = {
                "categories": category_serializer.data,
            }

            return standardResponse(status="success", message="Data retrieved", data=data)
        except Exception as e:
            return standardResponse(status="error", message=str(e), data={})

    @action(detail=True, methods=['GET'])
    def content(self, request, pk=None):
        try:
            category = Catagory.objects.get(id=pk)

            # Fetch and paginate movies related to this category
            movies_query = Movie.objects.filter(
                category=category).order_by('id')
            paginated_movies, movie_pagination_data = paginate_queryset(
                movies_query, request)
            if not paginated_movies:
                return Response({"status": "error", "message": "Invalid page for movies.", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch and paginate series related to this category
            series_query = Series.objects.filter(
                category=category).order_by('id')
            paginated_series, series_pagination_data = paginate_queryset(
                series_query, request)
            if not paginated_series:
                return Response({"status": "error", "message": "Invalid page for series.", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize movies and series
            movie_serializer = HomeMovieSerializer(
                paginated_movies, many=True, context={'request': request})
            series_serializer = SeriesListSerializer(
                paginated_series, many=True, context={'request': request})

            # Aggregate data
            data = {
                "movies": movie_serializer.data,
                "series": series_serializer.data,
                "movies_pagination": movie_pagination_data,
                "series_pagination": series_pagination_data
            }

            return Response({"status": "success", "message": "Data retrieved", "data": data}, status=status.HTTP_200_OK)
        except Catagory.DoesNotExist:
            return Response({"status": "error", "message": "Category not found", "data": {}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e), "data": {}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BannerViewSet(BaseViewSet):
    queryset = Banner.objects.filter(status=True)
    serializer_class = BannerSerializer


class SubscriptionPlanView(BaseViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer


class UserSubscriptionViewSet(BaseViewSet):
    """
    API endpoint that allows UserSubscriptions to be viewed or edited.
    """
    queryset = UserSubscription.objects.all().order_by('-start_date')
    serializer_class = UserSubscriptionSerializer


class FavoriteContentViewSet(BaseViewSet):
    queryset = FavoriteContent.objects.all()

    def list(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return standardResponse(status='error', message='Invalid or expired token', data=status.HTTP_401_UNAUTHORIZED)

        token = auth_header[1]
        user_info = decode_token(token)

        # Fetch favorite movies
        favorite_movies = FavoriteContent.objects.filter(
            username=user_info['username'],
            content_type=ContentType.objects.get_for_model(Movie)
        )
        movie_ids = [fav.object_id for fav in favorite_movies]
        movies_query = Movie.objects.filter(id__in=movie_ids).order_by("id")

        # Paginate movies
        paginated_movies, movie_pagination_data = paginate_queryset(
            movies_query, request)
        movie_serializer = MovieSerializer(
            paginated_movies, many=True, context={'request': request})

        # Fetch favorite series
        favorite_series = FavoriteContent.objects.filter(
            username=user_info['username'],
            content_type=ContentType.objects.get_for_model(Series)
        )
        series_ids = [fav.object_id for fav in favorite_series]
        series_query = Series.objects.filter(id__in=series_ids).order_by("id")

        # Paginate series
        paginated_series, series_pagination_data = paginate_queryset(
            series_query, request)
        series_serializer = SeriesSerializer(
            paginated_series, many=True, context={'request': request})

        # Combine data with pagination info
        data = {
            'movies': {
                'results': movie_serializer.data,
                'pagination': movie_pagination_data
            },
            'series': {
                'results': series_serializer.data,
                'pagination': series_pagination_data
            }
        }

        return standardResponse(status="success", message="Favorite movies and series retrieved", data=data)
