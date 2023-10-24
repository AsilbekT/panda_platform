from django.http import JsonResponse
from django.db.models import Q
from video_app.models import Movie, Series
from .utils import standardResponse
from rest_framework.views import APIView


class GeneralSearch(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        print(query)
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(genre__name__icontains=query)
        ).distinct()

        series = Series.objects.filter(
            Q(title__icontains=query) |
            Q(genre__name__icontains=query)
        ).distinct()

        movies_list = [movie.title for movie in movies]
        series_list = [serie.title for serie in series]
        data = {"movies": movies_list, "series": series_list}

        return standardResponse(status="success", message="Data fetched successfully", data=data)


class GenreSearch(APIView):
    def get(self, request):
        # Get the 'genres' query parameter and split it into a list
        genres = request.GET.get('genres', '').split(',')

        # Remove any leading/trailing whitespaces from each genre
        genres = [genre.strip() for genre in genres]

        # Create a Q object for OR-ing the filters together
        query = Q(genre__name__icontains=genres[0])
        for genre in genres[1:]:
            query |= Q(genre__name__icontains=genre)

        # Search in the Movie and Series models by genre
        movies = Movie.objects.filter(query).distinct()
        series = Series.objects.filter(query).distinct()

        # Serialize the data (for demonstration, we'll only send the titles)
        movies_list = [movie.title for movie in movies]
        series_list = [serie.title for serie in series]

        data = {"movies": movies_list, "series": series_list}

        return standardResponse(status="success", message="Data fetched successfully", data=data)
