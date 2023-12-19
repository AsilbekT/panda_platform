from rest_framework import viewsets
from video_app.models import (
    Banner, Catagory, Comment,
    Director, Episode, FavoriteContent,
    Season, Series, Genre,
    Movie, VideoConversionType
)
from .serializers import (
    BannerSerializer, CatagorySerializer,
    CommentSerializer, DirectorSerializer,
    EpisodeSerializer, FavoriteContentPlanSerializer,
    SeasonSerializer, SeriesSerializer,
    GenreSerializer, MovieSerializer,
    VideoConversionTypeSerializer
)
from video_app.utils import paginate_queryset

from video_app.utils import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CatagorySerializerViewSet(viewsets.ModelViewSet):
    queryset = Catagory.objects.all().order_by("id")
    serializer_class = CatagorySerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Catagiries retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Catagiries successfully deleted")


class FavoriteContentViewSet(viewsets.ModelViewSet):
    queryset = FavoriteContent.objects.all().order_by("id")
    serializer_class = FavoriteContentPlanSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Favirute Content retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Favorite content successfully deleted")


class VideoConversionTypeViewSet(viewsets.ModelViewSet):
    queryset = VideoConversionType.objects.all().order_by("id")
    serializer_class = VideoConversionTypeSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Video Conversion retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Video conversion successfully deleted")


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by("id")
    serializer_class = GenreSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Genres retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Genre successfully deleted")


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all().order_by("id")
    serializer_class = DirectorSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Directors retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Director successfully deleted")


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Movies retrieved", data=serializer.data, pagination=pagination_data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Movie successfully deleted")


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all().order_by("id")
    serializer_class = SeriesSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Series retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Series successfully deleted")


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by("id")
    serializer_class = SeasonSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Seasons retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Seoson successfully deleted")


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all().order_by("id")
    serializer_class = EpisodeSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Episodes retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Episode successfully deleted")


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by("id")
    serializer_class = BannerSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Banners retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Banner content successfully deleted")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("id")
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]  # JWT Authentication
    permission_classes = [IsAuthenticated]  # Permission class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Comments retrieved", data=serializer.data, pagination=pagination_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return standardResponse(status="success", message="Comment successfully deleted")
