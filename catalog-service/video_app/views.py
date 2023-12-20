from django.contrib.contenttypes.models import ContentType
from video_app.utils import MobileOnlyMixin, decode_token, standardResponse, user_has_active_plan
from .models import Catagory, Comment, Content, FavoriteContent, Genre, Director, Movie, Season, Series, Episode, Banner, SubscriptionPlan, UserSubscription, ContentType
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    EpisodeSerializerDetails,
    FavoriteContentSerializer,
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

from rest_framework import generics


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DirectorViewSet(BaseViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(MobileOnlyMixin, BaseViewSet):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.filter(is_ready=True)
        if not self.is_request_from_mobile(self.request):
            queryset = queryset.filter(is_mobile_only=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer

    def list(self, request, *args, **kwargs):
        genre_from_param = request.query_params.get('genre', None)
        queryset = self.get_queryset().filter(
            genre_id=genre_from_param) if genre_from_param else self.get_queryset()

        # Ensure the queryset is ordered
        # or any other field you want to order by
        queryset = queryset.order_by('id')

        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = self.get_serializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Movies retrieved", data=serializer.data, pagination=pagination_data)


class SeriesViewSet(MobileOnlyMixin, BaseViewSet):
    serializer_class = SeriesSerializer

    def get_queryset(self):
        queryset = Series.objects.filter(is_ready=True).order_by('id')
        genre_from_param = self.request.query_params.get('genre', None)

        if not self.is_request_from_mobile(self.request):
            queryset = queryset.filter(is_mobile_only=False)

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


class EpisodeViewSet(MobileOnlyMixin, BaseViewSet):
    queryset = Episode.objects.all().order_by('series', 'season', 'episode_number')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.is_request_from_mobile(self.request):
            queryset = queryset.filter(series__is_mobile_only=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return EpisodeSerializer
        elif self.action == 'retrieve':
            return EpisodeSerializerDetails
        return EpisodeSerializer

    def list(self, request, *args, **kwargs):
        series_id = kwargs.get('series_pk')
        season_id = kwargs.get('season_pk')

        # Filter queryset based on series_id, season_id and is_ready
        queryset = self.queryset.filter(is_ready=True)
        if series_id:
            queryset = queryset.filter(series_id=series_id)
        if season_id:
            queryset = queryset.filter(season_id=season_id)

        paginated_queryset, pagination_data = paginate_queryset(
            queryset, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        serializer = EpisodeSerializer(
            paginated_queryset, many=True, context={'request': request})
        return standardResponse(status="success", message="Episodes retrieved", data={'episodes': serializer.data, 'pagination': pagination_data})


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
    queryset = Catagory.objects.none()

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
            movies = Movie.objects.filter(category=category).order_by('id')
            series = Series.objects.filter(category=category).order_by('id')

            # Combine movies and series into a single queryset
            combined_content = list(movies) + list(series)

            # Paginate the combined list using your custom function
            paginated_queryset, pagination_data = paginate_queryset(
                combined_content, request)
            if not paginated_queryset:
                return standardResponse(status="error", message="Invalid page.", data={})

            # Serialize page items
            content_list = []
            for item in paginated_queryset:
                if isinstance(item, Movie):
                    serialized_item = HomeMovieSerializer(
                        item, context={'request': request}).data
                    serialized_item['is_movie'] = True
                else:
                    serialized_item = SeriesListSerializer(
                        item, context={'request': request}).data
                    serialized_item['is_movie'] = False
                content_list.append(serialized_item)

            # Return standard response with custom pagination
            return standardResponse(status="success", message="Contents retrieved", data={"content": content_list, "pagination": pagination_data})

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


class UserSubscriptionViewSet(BaseViewSet):
    """
    API endpoint that allows UserSubscriptions to be viewed or edited.
    """
    queryset = UserSubscription.objects.all().order_by('-start_date')
    serializer_class = UserSubscriptionSerializer


class FavoriteContentViewSet(BaseViewSet):
    queryset = FavoriteContent.objects.all()
    serializer_class = FavoriteContentSerializer

    def list(self, request, *args, **kwargs):
        # Validate the token
        auth_status, user_info, _ = self.validate_token(request)
        if not auth_status:
            return standardResponse(status='error', message='Invalid or expired token', data=status.HTTP_401_UNAUTHORIZED)

        # Fetch favorite movies and series
        favorite_content = FavoriteContent.objects.filter(
            username=user_info['username'])
        movie_ids = favorite_content.filter(content_type=ContentType.objects.get_for_model(
            Movie)).values_list('object_id', flat=True)
        series_ids = favorite_content.filter(content_type=ContentType.objects.get_for_model(
            Series)).values_list('object_id', flat=True)

        # Query movies and series
        movies_query = Movie.objects.filter(id__in=movie_ids).order_by("id")
        series_query = Series.objects.filter(id__in=series_ids).order_by("id")
        # Combine movies and series into a single queryset
        combined_content = list(movies_query) + list(series_query)

        # Paginate the combined list using your custom function
        paginated_queryset, pagination_data = paginate_queryset(
            combined_content, request)
        if not paginated_queryset:
            return standardResponse(status="error", message="Invalid page.", data={})

        # Serialize page items
        content_list = []
        for item in paginated_queryset:
            if isinstance(item, Movie):
                serialized_item = HomeMovieSerializer(
                    item, context={'request': request}).data
                serialized_item['is_movie'] = True
            else:
                serialized_item = SeriesListSerializer(
                    item, context={'request': request}).data
                serialized_item['is_movie'] = False
            content_list.append(serialized_item)

        # Return standard response with custom pagination
        return standardResponse(status="success", message="Contents retrieved", data={"content": content_list, "pagination": pagination_data})


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        content_type_str = self.request.data.get('content_type', '').lower()
        object_id = self.request.data.get('object_id')

        if not content_type_str or not object_id:
            return standardResponse('error', 'Missing content type or object ID', {}, status.HTTP_400_BAD_REQUEST)

        app_label = 'video_app'  # Replace with your actual app label

        try:
            content_type = ContentType.objects.get(
                app_label=app_label, model=content_type_str)
        except ContentType.DoesNotExist:
            return standardResponse('error', 'Invalid content type', {}, status.HTTP_400_BAD_REQUEST)

        username = self.get_username_from_token()
        serializer.save(username=username,
                        content_type=content_type, object_id=object_id)

    def get_username_from_token(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            token = auth_header[1]
            user_info = decode_token(token)
            return user_info.get('username', 'anonymous')
        return 'anonymous'

    def create(self, request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return standardResponse('error', 'Invalid or expired token', {}, status.HTTP_401_UNAUTHORIZED)

        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            return standardResponse('success', 'Comment created', response.data)
        return response

    def get_queryset(self):
        content_type_str = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        if content_type_str and object_id:
            app_label = 'video_app'  # Replace with your actual app label
            try:
                content_type = ContentType.objects.get(
                    app_label=app_label, model=content_type_str.lower())
                return Comment.objects.filter(content_type=content_type, object_id=object_id)
            except ContentType.DoesNotExist:
                pass  # Handle the exception as needed

        return Comment.objects.none()
