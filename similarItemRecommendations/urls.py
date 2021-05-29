from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchResult', views.searchMovieByTitle, name='searchMovieByTitle'),
]
