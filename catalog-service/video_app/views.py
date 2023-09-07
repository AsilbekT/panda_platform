from video_app.utils import standardResponse
from .models import Catagory, Genre, Director, Movie, Series, Episode, Banner
from rest_framework.views import APIView
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    DirectorSerializer,
    HomeAPIBannerSerializer,
    HomeGenreSerializer,
    HomeMovieSerializer,
    HomeSeriesSerializer,
    MovieSerializer,
    SeriesSerializer,
    EpisodeSerializer,
    BannerSerializer
)
from .base_view import BaseViewSet
from video_app.utils import paginate_queryset
from rest_framework.pagination import PageNumberPagination


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DirectorViewSet(BaseViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(BaseViewSet):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        genre_from_param = self.request.query_params.get('genre', None)
        queryset = self.queryset.filter(
            id=genre_from_param) if genre_from_param else self.queryset

        paginated_queryset, error_response = paginate_queryset(
            queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = MovieSerializer(
                paginated_queryset, many=True, context={'request': request})
            return standardResponse(status="success", message="Movies retrieved", data=serializer.data)
        return standardResponse(status="error", message="No movies found", data={})


class SeriesViewSet(BaseViewSet):
    queryset = Series.objects.all().order_by('id')
    serializer_class = SeriesSerializer

    def list(self, request, *args, **kwargs):
        genre_from_param = self.request.query_params.get('genre', None)
        queryset = self.queryset.filter(
            id=genre_from_param) if genre_from_param else self.queryset

        paginated_queryset, error_response = paginate_queryset(
            queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = SeriesSerializer(
                paginated_queryset, many=True, context={'request': request})
            return standardResponse(status="success", message="Series retrieved", data=serializer.data)
        return standardResponse(status="error", message="No series found", data={})


class EpisodeViewSet(BaseViewSet):
    queryset = Episode.objects.all().order_by('series', 'season', 'episode_number')
    serializer_class = EpisodeSerializer

    def list(self, request, series_id=None, *args, **kwargs):
        queryset = self.queryset.filter(
            series_id=series_id) if series_id else self.queryset

        paginated_queryset, error_response = paginate_queryset(
            queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = EpisodeSerializer(
                paginated_queryset, many=True, context={'request': request})
            return standardResponse(status="success", message="Episodes retrieved", data=serializer.data)
        return standardResponse(status="error", message="No episodes found", data={})


class HomeAPIView(APIView):
    def get_content_by_category(self, request):
        categories = Catagory.objects.all()
        category_data = {}

        for category in categories:
            movies = Movie.objects.filter(category=category)
            series = Series.objects.filter(category=category)
            movie_serializer = HomeMovieSerializer(
                movies, many=True, context={'request': request})
            series_serializer = HomeSeriesSerializer(
                series, many=True, context={'request': request})

            category_data[category.name] = {
                "movies": movie_serializer.data,
                "series": series_serializer.data
            }

        return category_data

    def get(self, request, *args, **kwargs):
        try:

            # Get featured movies
            featured_movies = Movie.objects.filter(
                is_featured=True).order_by("id")
            paginated_movies, error_response = paginate_queryset(
                featured_movies, request)
            if error_response:
                return error_response
            movie_serializer = HomeMovieSerializer(
                paginated_movies, many=True, context={'request': request})

            # Get featured series
            featured_series = Series.objects.filter(
                is_featured=True).order_by("id")
            paginated_series, error_response = paginate_queryset(
                featured_series, request)
            if error_response:
                return error_response
            series_serializer = HomeSeriesSerializer(
                paginated_series, many=True, context={'request': request})

            # Get all genres
            genres = Genre.objects.all()
            genre_serializer = GenreSerializer(
                genres, many=True, context={'request': request})

            category_data = self.get_content_by_category(request=request)
            # Get top directors (you might need to add a method to filter top directors)
            top_directors = Director.objects.all()[:5]

            director_serializer = DirectorSerializer(
                top_directors, many=True, context={'request': request})

            # Get banners (new addition)
            banners = Banner.objects.filter(status=True)
            banner_serializer = HomeAPIBannerSerializer(
                banners, many=True, context={'request': request})

            # Aggregate data
            data = {
                "featured_movies": movie_serializer.data,
                "featured_series": series_serializer.data,
                "genres": genre_serializer.data,
                "top_directors": director_serializer.data,
                "categories": category_data,
                "banners": banner_serializer.data  # new addition
            }

            return standardResponse(status="success", message="Data retrieved", data=data)
        except Exception as e:
            return standardResponse(status="error", message=str(e), data={})


class BannerViewSet(BaseViewSet):
    queryset = Banner.objects.filter(status=True)
    serializer_class = BannerSerializer
