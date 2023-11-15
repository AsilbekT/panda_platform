from rest_framework import serializers
from .models import Catagory, Comment, FavoriteContent, Genre, Director, Movie, Season, Series, Episode, Banner, SubscriptionPlan, UserSubscription
from django.contrib.contenttypes.models import ContentType


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'release_date', 'genre', 'is_free', 'rating',
            'is_premiere', 'trailer_url', 'thumbnail_image'
        ]

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class SeriesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    seasons = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = '__all__'

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)

    def get_seasons(self, obj):
        seasons = Season.objects.filter(series=obj)
        return SeasonSerializer(seasons, many=True, context=self.context).data


class SeriesDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    seasons = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = '__all__'

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)

    def get_seasons(self, obj):
        seasons = Season.objects.filter(series=obj)
        return SeasonSerializer(seasons, many=True, context=self.context).data


class SeriesListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = [
            'id', 'title', 'release_date', 'genre', 'is_free',
            'is_premiere', 'series_summary_url', 'thumbnail_image', 'description'
        ]

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class EpisodeSerializer(serializers.ModelSerializer):
    series_description = serializers.ReadOnlyField(source='series.description')
    series_genre_name = serializers.ReadOnlyField(source='series.genre.name')

    class Meta:
        model = Episode
        fields = [
            'series',
            'season',
            'episode_number',
            'title',
            'duration_minute',
            'thumbnail_image_url',
            'series_description',
            'series_genre_name'
        ]


class EpisodeSerializerDetails(serializers.ModelSerializer):
    series_description = serializers.ReadOnlyField(source='series.description')
    series_genre_name = serializers.ReadOnlyField(source='series.genre.name')

    class Meta:
        model = Episode
        fields = [
            'series',
            'season',
            'episode_number',
            'title',
            'duration_minute',
            'episode_content_url',
            'thumbnail_image_url',
            'series_description',
            'series_genre_name'
        ]


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'season_number', 'trailer_url',
                  'thumbnail_image']


class SeasonWithEpisodesSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = ['id', 'season_number', 'trailer_url',
                  'thumbnail_image', 'episodes']

    def get_episodes(self, obj):
        episodes = Episode.objects.filter(season=obj)
        return EpisodeSerializer(episodes, many=True, context=self.context).data


class BannerSerializer(serializers.ModelSerializer):
    trailer_url = serializers.CharField(read_only=True)
    thumbnail_image_url = serializers.CharField(
        read_only=True)
    content_title = serializers.CharField(
        read_only=True)
    content_genre = GenreSerializer(
        source='content_object.genre', many=True, read_only=True)
    description = serializers.SerializerMethodField()
    release_year = serializers.IntegerField(
        read_only=True)
    rating = serializers.FloatField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Banner
        fields = [
            'id', 'name', 'is_premiere',
            'content_type', 'object_id', 'content_genre', 'trailer_url',
            'thumbnail_image_url', 'content_title', 'release_year',
            'rating', 'priority', 'status', 'description',
            'created_at', 'updated_at', 'is_movie'
        ]

    def get_description(self, obj):
        content_object = obj.content_object
        return getattr(content_object, 'description', None) if content_object else None


class HomeAPIBannerSerializer(serializers.ModelSerializer):
    trailer_url = serializers.CharField(read_only=True)
    thumbnail_image_url = serializers.CharField(
        read_only=True)
    content_title = serializers.CharField(
        read_only=True)
    release_year = serializers.IntegerField(
        read_only=True)
    rating = serializers.FloatField(read_only=True)
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['trailer_url', 'thumbnail_image_url',
                  'content_title', 'release_year', 'rating', 'genre']

    def get_genre(self, obj):
        if obj.content_object:
            return GenreSerializer(obj.content_object.genre).data
        return None


class HomeMovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    year = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'genre', 'director', 'rating',
                  'thumbnail_image', 'year', 'title', 'is_premiere', 'description', 'trailer_url']

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class HomeSeriesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    year = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'genre', 'director', 'rating',
                  'thumbnail_image', 'year', 'title', 'is_premiere']

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = '__all__'


class HomeGenreSerializer(serializers.ModelSerializer):
    movies = HomeMovieSerializer(source='movie_contents', many=True)
    series = HomeSeriesSerializer(many=True, source='series_contents')

    class Meta:
        model = Genre
        fields = ['id', 'name', 'movies', 'series']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price', 'duration_days']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['id', 'user_id', 'username', 'subscription_plan_name',
                  'start_date', 'end_date', 'status']


class FavoriteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteContent
        fields = ['id', 'content_object']


class CommentSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'object_id',
                  'content_type', 'parent', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_content_type(self, value):
        app_label = 'video_app'  # Assuming 'video_app' is the app label
        try:
            # Convert the string to a ContentType instance
            return ContentType.objects.get(app_label=app_label, model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError('Invalid content type')

    def create(self, validated_data):
        # Extract content_type and object_id from validated_data
        content_type = validated_data.pop('content_type')
        object_id = validated_data.pop('object_id')

        # Create the Comment instance
        return Comment.objects.create(content_type=content_type, object_id=object_id, **validated_data)

    def get_comment_count(self, obj):
        content_type = ContentType.objects.get_for_model(Movie)
        return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()
