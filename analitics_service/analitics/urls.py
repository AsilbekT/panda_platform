# urls.py in your Django project or app

from django.urls import path
from .views import (
    TotalRevenueView,
    TotalReviewsView,
    TotalWatchDurationView,
    user_watch_data_view,

)


urlpatterns = [
    path('record-watch-data/', user_watch_data_view, name='record-watch-data'),
    path('content/<int:content_id>/total-watch-duration/',
         TotalWatchDurationView.as_view()),

    # URL for total reviews and average rating of content
    path('content/<int:content_id>/total-reviews/', TotalReviewsView.as_view()),

    # URL for total revenue
    path('revenue/total/', TotalRevenueView.as_view()),
]
