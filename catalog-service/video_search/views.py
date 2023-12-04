from django.db.models.functions import ExtractYear
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from video_app.models import Movie, Series
from video_app.utils import standardResponse, paginate_queryset
from django.db.models import Q


class AdvancedSearch(APIView):
    def get(self, request):
        # Search and filtering parameters
        query = request.GET.get('q', '')
        genre = request.GET.get('genre', '')
        director = request.GET.get('director', '')
        min_rating = request.GET.get('min_rating', None)
        max_rating = request.GET.get('max_rating', None)
        start_year = request.GET.get('start_year', None)
        end_year = request.GET.get('end_year', None)

        # Building the query for movies and series
        movie_query = Q(title__icontains=query)
        series_query = Q(title__icontains=query)

        if genre:
            movie_query &= Q(genre__name__icontains=genre)
            series_query &= Q(genre__name__icontains=genre)

        if director:
            movie_query &= Q(director__name__icontains=director)
            series_query &= Q(director__name__icontains=director)

        if min_rating:
            movie_query &= Q(rating__gte=min_rating)
            series_query &= Q(rating__gte=min_rating)

        if max_rating:
            movie_query &= Q(rating__lte=max_rating)
            series_query &= Q(rating__lte=max_rating)

        if start_year:
            try:
                start_year = int(start_year)
                movie_query &= Q(release_date__year__gte=start_year)
                series_query &= Q(release_date__year__gte=start_year)
            except ValueError:
                # Handle invalid start_year value
                pass

        if end_year:
            try:
                end_year = int(end_year)
                movie_query &= Q(release_date__year__lte=end_year)
                series_query &= Q(release_date__year__lte=end_year)
            except ValueError:
                # Handle invalid end_year value
                pass

        # Fetching results
        movies = Movie.objects.filter(movie_query).distinct()
        series = Series.objects.filter(series_query).distinct()

        # Combining and paginating results
        combined_results = list(movies) + list(series)
        paginated_results, pagination_data = paginate_queryset(
            combined_results, request)

        # Serialize the data
        data_list = [{
            "id": item.id,
            "title": item.title,
            "type": "Movie" if isinstance(item, Movie) else "Series",
            "release_date": item.release_date,
            "genre": [genre.name for genre in item.genre.all()],
            "director": item.director.name,
            "thumbnail": self.build_absolute_uri(item.thumbnail_image.url) if item.thumbnail_image else None,
            "rating": item.rating
        } for item in paginated_results]
        return standardResponse(status="success", message="Data fetched successfully", data={"content": data_list, "pagination": pagination_data})

    def build_absolute_uri(self, relative_url):
        current_site = get_current_site(self.request)
        absolute_url = 'https://' + current_site.domain + relative_url
        return absolute_url


class AvailableYearsView(APIView):
    def get(self, request):
        movie_years = Movie.objects.annotate(year=ExtractYear(
            'release_date')).values_list('year', flat=True).distinct()
        series_years = Series.objects.annotate(year=ExtractYear(
            'release_date')).values_list('year', flat=True).distinct()
        combined_years = set(list(movie_years) + list(series_years))
        available_years = sorted(list(combined_years))

        data = {
            "available_years": available_years
        }
        return standardResponse(status="success", message="Data fetched successfully", data=data)
