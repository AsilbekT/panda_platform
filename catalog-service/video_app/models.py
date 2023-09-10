from django.db import models
from .utils import validate_file_size, validate_image_file
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Model for storing different genres


class VideoConversionType(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('MOVIE', 'Movie'),
        ('MOVIE_TRAILER', 'Movie Trailer'),
        ('SERIES', 'Series'),
        ('SERIES_TRAILER', 'Series Trailer'),
    ]

    video_type = models.CharField(
        max_length=20, choices=VIDEO_TYPE_CHOICES, unique=True)

    class Meta:
        db_table = 'video_conversion_type_table'

    def __str__(self):
        return self.video_type


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'genre_table'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'director_table'

    def __str__(self):
        return self.name


class Catagory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Catagory, on_delete=models.CASCADE, related_name="%(class)s_catagory", null=True, blank=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="%(class)s_contents")
    release_date = models.DateField(blank=True, null=True)
    duration_minute = models.IntegerField()
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, related_name="%(class)s_contents")
    cast_list = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    thumbnail_image = models.ImageField(
        upload_to="thumbnail_image/",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_file]
    )
    trailer_url = models.URLField(blank=True, null=True)

    main_content_url = models.URLField(blank=True, null=True, unique=True)

    is_ready = models.BooleanField(default=False)
    is_premiere = models.BooleanField(default=False)
    has_trailer = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Movie(Content):
    production_cost = models.FloatField(blank=True, null=True)
    licensing_cost = models.FloatField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    conversion_type = models.ForeignKey(
        VideoConversionType, on_delete=models.SET_NULL, null=True, related_name='movies')

    class Meta(Content.Meta):
        db_table = 'movie_table'

    def __str__(self):
        return f"Movie: {self.title}"


class Series(Content):
    main_content_url = None
    series_summary_url = models.URLField(blank=True, null=True)
    number_of_seasons = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    conversion_type = models.ForeignKey(
        VideoConversionType, on_delete=models.SET_NULL, null=True, related_name='series')

    class Meta(Content.Meta):
        db_table = 'series_table'

    def __str__(self):
        return f"Series: {self.title}"


class Season(models.Model):
    series = models.ForeignKey(
        Series, related_name='seasons', on_delete=models.CASCADE)
    season_number = models.IntegerField()
    trailer_url = models.URLField(blank=True, null=True)
    thumbnail_image = models.ImageField(
        upload_to="season_thumbnail_image/",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_file]
    )

    class Meta:
        db_table = 'season_table'
        unique_together = (('series', 'season_number'),)

    def __str__(self):
        return f"Season {self.season_number} of {self.series.title}"


class Episode(models.Model):
    series = models.ForeignKey(
        Series, related_name='episodes', on_delete=models.CASCADE)
    season = models.ForeignKey(
        Season, related_name='episodes', on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    duration_minute = models.IntegerField()
    thumbnail_image_url = models.URLField(blank=True, null=True)

    episode_content_url = models.URLField(unique=True)

    class Meta:
        db_table = 'episode_table'

    def __str__(self):
        return f"S{self.season.season_number}E{self.episode_number} - {self.title} of {self.series.title}"


class Banner(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=models.Q(app_label='video_app', model='movie') | models.Q(
            app_label='video_app', model='series')
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_movie = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banner_table'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.name

    @property
    def trailer_url(self):
        return getattr(self.content_object, 'trailer_url', None)

    @property
    def thumbnail_image_url(self):
        if self.content_object and hasattr(self.content_object, 'thumbnail_image'):
            return self.content_object.thumbnail_image.url if self.content_object.thumbnail_image else None
        return None

    @property
    def content_title(self):
        return getattr(self.content_object, 'title', None)

    @property
    def release_year(self):
        release_date = getattr(self.content_object, 'release_date', None)
        return release_date.year if release_date else None

    @property
    def rating(self):
        return getattr(self.content_object, 'rating', None)

    @property
    def is_premiere(self):
        return getattr(self.content_object, 'is_premiere', None)
