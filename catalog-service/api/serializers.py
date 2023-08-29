from rest_framework import serializers
from .models import Genre, Director, Movie, Series, Episode

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
    
    class Meta:
        model = Movie
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)

    class Meta:
        model = Series
        fields = '__all__'

class EpisodeSerializer(serializers.ModelSerializer):
    # series_description = serializers.ReadOnlyField(source='series.description')
    # series_genre_name = serializers.ReadOnlyField(source='series.genre.name')

    class Meta:
        model = Episode
        fields = [
            'series', 
            'season', 
            'episode_number', 
            'title', 
            'duration_minute', 
            'main_content_url', 
            # 'series_description',
            # 'series_genre_name'
        ]