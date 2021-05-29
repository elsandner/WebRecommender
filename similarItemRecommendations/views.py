from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


def index(request):
    template = loader.get_template('similarItemRecommendations/index.html')
    context = {
        'userId': '1',
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def searchMovieByTitle(request):
    template = loader.get_template('similarItemRecommendations/searchResult.html')
    context = {
        'data': "recommendationDict",
        'userId': "userId",
    }
    return HttpResponse(template.render(context))