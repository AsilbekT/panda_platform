from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.AdvancedSearch.as_view(), name='general_search'),
]
