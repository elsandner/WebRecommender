from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from similarItemRecommendations import similarItemService
from similarItemRecommendations.util import create_merged_ratings_df

from recommenderSystem.forms import NameForm    # TODO: whats this NameForm??!

metadata_DF = similarItemService.loadDF("archive/movies_metadata.csv")
keywords_DF = similarItemService.loadDF("archive/keywords.csv") 
ratings_DF = similarItemService.loadDF("archive/ratings.csv")
credits_DF = similarItemService.loadDF("archive/credits.csv")
merged_ratings_DF = None #INITIALIZING THE MERGED DF
try: 
    merged_ratings_DF = similarItemService.loadDF("archive/merged_ratings.csv")
except: 
    print("WARNING: merged_ratings.csv doesn't exist. (Normal if it's the first time running the server) \n Creating a new merged_ratings.csv It will take a few minutes...")
    create_merged_ratings_df(metadata_DF,ratings_DF)

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
        print("movieTitle")
        print(movieTitle)
        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 1, metadata_DF, keywords_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))


@csrf_exempt
def showMoviesByGenres(request):
    print("calculating movies by genres...")
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        movieTitle = metadata_DF.loc[metadata_DF['id'] == movieId].iloc[0]['title']
        print("movieTitle")
        print(movieTitle)
        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 2, metadata_DF, keywords_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))


@csrf_exempt
def showMoviesByDirectors(request):
    print("calculating movies by directors...")
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        movieTitle = metadata_DF.loc[metadata_DF['id'] == movieId].iloc[0]['title']
        print("movieTitle")
        print(movieTitle)
        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 3, metadata_DF, keywords_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))

@csrf_exempt
def showMoviesByActors(request):
    print("calculating similar actors...")
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        movieTitle = metadata_DF.loc[metadata_DF['id'] == movieId].iloc[0]['title']
        print("movieTitle")
        print(movieTitle)
        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 4, metadata_DF, credits_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))

@csrf_exempt
def showMoviesByRatings(request):
    print("calculating similar ratings...")
    if request.method == 'POST':
        form = NameForm(request.POST)  # TODO: works but seems to be bad practice ...
        movieId = form.data.get("movieId")

        movieTitle = metadata_DF.loc[metadata_DF['id'] == movieId].iloc[0]['title']
        print("movieTitle")
        print(movieTitle)
        similarMoviesDict = similarItemService.getSimilarMovies(movieId, 5, merged_ratings_DF, keywords_DF)

        template = loader.get_template('similarItemRecommendations/similarMovies.html')
        context = {
            'movieTitle': movieTitle,
            'searchMovie': similarMoviesDict,


        }
        return HttpResponse(template.render(context))

