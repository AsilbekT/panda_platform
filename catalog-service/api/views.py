from api.utils import standardResponse
from .models import Genre, Director, Movie, Series, Episode
from .serializers import (
    GenreSerializer, 
    DirectorSerializer, 
    MovieSerializer, 
    SeriesSerializer,
    EpisodeSerializer
    )
from .base_view import BaseViewSet
from api.utils import paginate_queryset


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
        queryset = self.queryset.filter(genre__name=genre_from_param) if genre_from_param else self.queryset

        paginated_queryset, error_response = paginate_queryset(queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = MovieSerializer(paginated_queryset, many=True)
            return standardResponse(status="success", message="Movies retrieved", data=serializer.data)
        return standardResponse(status="error", message="No movies found", data={})


class SeriesViewSet(BaseViewSet):
    queryset = Series.objects.all().order_by('id')
    serializer_class = SeriesSerializer

    def list(self, request, *args, **kwargs):
        genre_from_param = self.request.query_params.get('genre', None)
        queryset = self.queryset.filter(genre__name=genre_from_param) if genre_from_param else self.queryset

        paginated_queryset, error_response = paginate_queryset(queryset, request)
        if error_response:
            return error_response

        if paginated_queryset:
            serializer = SeriesSerializer(paginated_queryset, many=True)
            return standardResponse(status="success", message="Series retrieved", data=serializer.data)
        return standardResponse(status="error", message="No series found", data={})


class EpisodeViewSet(BaseViewSet):
    queryset = Episode.objects.all().order_by('series', 'season', 'episode_number')
    serializer_class = EpisodeSerializer

    def list(self, request,series_id=None, *args, **kwargs):
        queryset = self.queryset.filter(series_id=series_id) if series_id else self.queryset
   
        paginated_queryset, error_response = paginate_queryset(queryset, request)
        if error_response:
            return error_response
        
        if paginated_queryset:
            serializer = EpisodeSerializer(paginated_queryset, many=True)
            return standardResponse(status="success", message="Episodes retrieved", data=serializer.data)
        return standardResponse(status="error", message="No episodes found", data={})
