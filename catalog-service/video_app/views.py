from django.contrib.contenttypes.models import ContentType
from video_app.utils import decode_token, standardResponse, user_has_active_plan
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

            # Paginate the combined queryset
            page = self.paginate_queryset(combined_content)
            if page is not None:
                # Serialize page items
                content_list = []
                for item in page:
                    if isinstance(item, Movie):
                        serialized_item = HomeMovieSerializer(
                            item, context={'request': request}).data
                        serialized_item['is_movie'] = True
                    else:
                        serialized_item = SeriesListSerializer(
                            item, context={'request': request}).data
                        serialized_item['is_movie'] = False
                    content_list.append(serialized_item)

                pagination_data = {
                    "total": self.paginator.page.paginator.count,
                    "page_size": self.paginator.page_size,
                    "current_page": self.paginator.page.number,
                    "total_pages": self.paginator.page.paginator.num_pages,
                    "next": self.paginator.get_next_link() is not None,
                    "previous": self.paginator.get_previous_link() is not None
                }

                # Return standard response with custom pagination
                return standardResponse(status="success", message="Data retrieved", data={"content": content_list, "pagination": pagination_data})

            # Fallback if pagination is not applicable
            return standardResponse(status="error", message="Pagination error", data={})
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
        combined_content = list(movies_query) + list(series_query)

        # Paginate the combined queryset
        page = self.paginate_queryset(combined_content)

        if page is not None:
            # Serialize page items
            content_list = []
            for item in page:
                if isinstance(item, Movie):
                    serialized_item = HomeMovieSerializer(
                        item, context={'request': request}).data
                    serialized_item['is_movie'] = True
                else:
                    serialized_item = SeriesListSerializer(
                        item, context={'request': request}).data
                    serialized_item['is_movie'] = False
                content_list.append(serialized_item)

            pagination_data = {
                "total": self.paginator.page.paginator.count,
                "page_size": self.paginator.page_size,
                "current_page": self.paginator.page.number,
                "total_pages": self.paginator.page.paginator.num_pages,
                "next": self.paginator.get_next_link() is not None,
                "previous": self.paginator.get_previous_link() is not None
            }
            return standardResponse(status="success", message="Data retrieved", data={"content": content_list, "pagination": pagination_data})


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        content_type_str = self.request.data.get('content_type').lower()
        object_id = self.request.data.get('object_id')

        # Assuming 'video_app' is the app label
        app_label = 'video_app'

        try:
            # Fetch the ContentType based on app_label and model
            content_type = ContentType.objects.get(
                app_label=app_label, model=content_type_str)
        except ContentType.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Invalid content type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Fetch the username from the token
        username = self.get_username_from_token()

        # Save the comment with the fetched ContentType and object_id
        serializer.save(username=username,
                        content_type=content_type, object_id=object_id)

    def get_username_from_token(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) == 2 and auth_header[0].lower() == 'bearer':
            token = auth_header[1]
            user_info = decode_token(token)
            # Ensure 'username' is a key in the token payload
            return user_info.get('username')
        return 'anonymous'

    def create(self, request, *args, **kwargs):
        # Override the create method to add custom response for token errors
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return Response(
                {'status': 'error', 'message': 'Invalid or expired token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        content_type_str = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        if content_type_str and object_id:
            app_label = 'video_app'  # Assuming 'video_app' is the app label
            try:
                content_type = ContentType.objects.get(
                    app_label=app_label, model=content_type_str.lower())
                return Comment.objects.filter(content_type=content_type, object_id=object_id)
            except ContentType.DoesNotExist:
                pass  # Handle the exception as needed

        return Comment.objects.none()
