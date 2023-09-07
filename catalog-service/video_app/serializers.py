from rest_framework import serializers
from .models import Catagory, Genre, Director, Movie, Series, Episode, Banner


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
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
    genre = GenreSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = Series
        fields = '__all__'

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
            'main_content_url',
            'thumbnail_image_url',
            'series_description',
            'series_genre_name'
        ]


class BannerSerializer(serializers.ModelSerializer):
    trailer_url = serializers.CharField(read_only=True)
    thumbnail_image_url = serializers.CharField(
        read_only=True)
    content_title = serializers.CharField(
        read_only=True)
    release_year = serializers.IntegerField(
        read_only=True)
    rating = serializers.FloatField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Banner
        fields = ['id', 'name', 'is_premiere', 'content_type', 'object_id', 'trailer_url', 'thumbnail_image_url',
                  'content_title', 'release_year', 'rating', 'priority', 'status', 'created_at', 'updated_at']


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
    genre = GenreSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    year = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'genre', 'director',
                  'thumbnail_image', 'year', 'title', 'is_premiere']

    def get_thumbnail_image(self, obj):
        request = self.context.get('request')
        thumbnail_image_url = obj.thumbnail_image.url
        return request.build_absolute_uri(thumbnail_image_url)


class HomeSeriesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)
    thumbnail_image = serializers.SerializerMethodField()
    year = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    is_premiere = serializers.BooleanField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'genre', 'director',
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
