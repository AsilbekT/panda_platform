from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.GeneralSearch.as_view(), name='general_search'),
    path('search/genre/', views.GenreSearch.as_view(), name='genre_search'),
]
