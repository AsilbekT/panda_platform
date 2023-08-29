from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="%(class)s_contents")
    release_date = models.DateField(blank=True, null=True)
    duration_minute = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name="%(class)s_contents")
    cast_list = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    thumbnail_image_url = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    main_content_url = models.URLField(unique=True)

    is_ready = models.BooleanField(default=False)
    is_premiere = models.BooleanField(default=False)
    has_trailer = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Movie(Content):
    production_cost = models.FloatField(blank=True, null=True)
    licensing_cost = models.FloatField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return f"Movie: {self.title}"

class Series(Content):
    number_of_seasons = models.IntegerField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return f"Series: {self.title}"

class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='episodes', on_delete=models.CASCADE)
    season = models.IntegerField()
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255)
    duration_minute = models.IntegerField()
    main_content_url = models.URLField(unique=True)

    def __str__(self):
        return f"S{self.season}E{self.episode_number} - {self.title} of {self.series.title}"
