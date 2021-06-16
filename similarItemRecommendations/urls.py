from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchResult', views.searchMovieByTitle, name='searchMovieByTitle'),
    path('similarMovies', views.showSimilarMovies, name='showSimilarMovies'),
    path('moviesByGenres', views.showMoviesByGenres, name='showMoviesByGenres'),
    path('moviesByDirectors', views.showMoviesByDirectors, name='showMoviesByDirectors'),
    path('moviesByRatings', views.showMoviesByRatings, name='showMoviesByRatings'),
    path('moviesByActors', views.showMoviesByActors, name='showMoviesByActors')
]
