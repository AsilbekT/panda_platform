from video_app.utils import standardResponse
from .models import Catagory, Genre, Director, Movie, Season, Series, Episode, Banner, SubscriptionPlan
from .serializers import (
    CategorySerializer,
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
    SubscriptionPlanSerializer
)
from .base_view import BaseViewSet
from video_app.utils import paginate_queryset
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DirectorViewSet(BaseViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(BaseViewSet):
    queryset = Movie.objects.all().order_by('id')

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

        paginated_queryset, error_response = paginate_queryset(
            queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = self.get_serializer(
                paginated_queryset, many=True, context={'request': request})
            return standardResponse(status="success", message="Movies retrieved", data=serializer.data)
        return standardResponse(status="error", message="No movies found", data={})


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
        paginated_queryset, error_response = paginate_queryset(
            queryset, request)
        if error_response:
            return error_response

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Series retrieved", data=serializer.data)


class EpisodeViewSet(BaseViewSet):
    queryset = Episode.objects.all().order_by('series', 'season', 'episode_number')
    serializer_class = EpisodeSerializer

    def list(self, request, series_id=None, *args, **kwargs):
        queryset = self.queryset.filter(
            series_id=series_id) if series_id else self.queryset

        paginated_queryset, error_response = paginate_queryset(
            queryset, request
        )
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = EpisodeSerializer(
                paginated_queryset, many=True, context={'request': request}
            )
            return standardResponse(status="success", message="Episodes retrieved", data=serializer.data)
        return standardResponse(status="error", message="No episodes found", data={})


class SeasonViewSet(BaseViewSet):
    queryset = Season.objects.all().order_by('season_number')

    def get_serializer_class(self):
        if self.action == 'list':
            return SeasonSerializer
        elif self.action == 'retrieve':
            return SeasonWithEpisodesSerializer
        return SeasonSerializer


class CategoryViewSet(BaseViewSet):
    serializer_class = CategorySerializer  # Add this line

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

            # Fetch movies and series related to this category
            movies = Movie.objects.filter(category=category)
            series = Series.objects.filter(category=category)

            # Serialize movies and series
            movie_serializer = HomeMovieSerializer(
                movies, many=True, context={'request': request})
            series_serializer = SeriesListSerializer(
                series, many=True, context={'request': request})

            # Aggregate data
            data = {
                "movies": movie_serializer.data,
                "series": series_serializer.data
            }

            return standardResponse(status="success", message="Data retrieved", data=data)
        except Catagory.DoesNotExist:
            return standardResponse(status="error", message="Category not found", data={})
        except Exception as e:
            return standardResponse(status="error", message=str(e), data={})


class BannerViewSet(BaseViewSet):
    queryset = Banner.objects.filter(status=True)
    serializer_class = BannerSerializer


class SubscriptionPlanView(BaseViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
