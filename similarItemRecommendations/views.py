from django.forms import forms
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from similarItemRecommendations import similarItemService

from recommenderSystem.forms import NameForm # TODO: whats this NameForm??!


def index(request):
    template = loader.get_template('similarItemRecommendations/index.html')
    context = {
        'Title': 'Enter a Title to search for it',
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def searchMovieByTitle(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = NameForm(request.POST)   # TODO: works but seems to be bad practice ...
        title = form.data.get("title")

        searchMoviesDict = similarItemService.searchMovies(title)

        template = loader.get_template('similarItemRecommendations/searchResult.html')
        context = {
            'searchMovies': searchMoviesDict,
            'searchTitle': title
        }
        return HttpResponse(template.render(context))


@csrf_exempt
def showSimilarMovies(request):
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 1)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'searchMovie': similarMoviesDict,
            'movieId': movieId

        }
        return HttpResponse(template.render(context))