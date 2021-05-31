from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from similarItemRecommendations import similarItemService

from recommenderSystem.forms import NameForm    # TODO: whats this NameForm??!

metadata_DF = similarItemService.loadDF("archive/movies_metadata.csv")
keywords_DF = similarItemService.loadDF("archive/keywords.csv")

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

        searchMoviesDict = similarItemService.searchMovies(title, metadata_DF)

        template = loader.get_template('similarItemRecommendations/searchResult.html')
        context = {
            'searchMovies': searchMoviesDict,
            'searchTitle': title
        }
        return HttpResponse(template.render(context))


@csrf_exempt
def showSimilarMovies(request):
    print("calculating similar items...")
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        movieTitle = metadata_DF.loc[metadata_DF['id'] == movieId].iloc[0]['title']

        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 1, metadata_DF, keywords_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))