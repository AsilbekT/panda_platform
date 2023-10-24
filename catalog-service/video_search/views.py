from django.http import JsonResponse
from django.db.models import Q
from video_app.models import Movie, Series, Director, Genre
from .utils import standardResponse
from rest_framework.views import APIView


class GeneralSearch(APIView):
    def get(self, request):
        query = request.GET.get('q', '')

        movies = Movie.objects.filter(
            Q(title__icontains=query)
        ).distinct()

        series = Series.objects.filter(
            Q(title__icontains=query)
        ).distinct()

        # Serialize the data
        movies_list = [{
            "id": movie.id,
            "title": movie.title,
            "release_date": movie.release_date,
            "genre": [genre.name for genre in movie.genre.all()],
            "director": movie.director.name,
            "thumbnail": movie.thumbnail_image.url if movie.thumbnail_image else None,
            "rating": movie.rating
        } for movie in movies]

        series_list = [{
            "id": serie.id,
            "title": serie.title,
            "release_date": serie.release_date,
            "genre": [genre.name for genre in serie.genre.all()],
            "director": serie.director.name,
            "thumbnail": serie.thumbnail_image.url if serie.thumbnail_image else None,
            "rating": serie.rating
        } for serie in series]

        data = {"movies": movies_list, "series": series_list}

        return JsonResponse({"status": "success", "message": "Data fetched successfully", "data": data})


class GenreSearch(APIView):
    def get(self, request):
        genres = request.GET.get('genres', '').split(',')
        genres = [genre.strip() for genre in genres]

        query = Q(genre__name__icontains=genres[0])
        for genre in genres[1:]:
            query |= Q(genre__name__icontains=genre)

        movies = Movie.objects.filter(query).distinct()
        series = Series.objects.filter(query).distinct()

        # Serialize the data (similar to the GeneralSearch class)
        movies_list = [{
            "id": movie.id,
            "title": movie.title,
            "release_date": movie.release_date,
            "genre": [genre.name for genre in movie.genre.all()],
            "director": movie.director.name,
            "thumbnail": movie.thumbnail_image.url if movie.thumbnail_image else None,
            "rating": movie.rating
        } for movie in movies]

        series_list = [{
            "id": serie.id,
            "title": serie.title,
            "release_date": serie.release_date,
            "genre": [genre.name for genre in serie.genre.all()],
            "director": serie.director.name,
            "thumbnail": serie.thumbnail_image.url if serie.thumbnail_image else None,
            "rating": serie.rating
        } for serie in series]

        data = {"movies": movies_list, "series": series_list}

        return JsonResponse({"status": "success", "message": "Data fetched successfully", "data": data})
