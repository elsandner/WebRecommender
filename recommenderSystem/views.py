import pandas
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm
from django.views.decorators.csrf import csrf_exempt
from recommenderSystem import nearestNeighbor


# index is executed when loading http://127.0.0.1:8000/rs/
@csrf_exempt
def index(request):
    template = loader.get_template('recommenderSystem/index.html')
    context = {
        'userId': '1',
    }
    return HttpResponse(template.render(context))


# function executed on button click
@csrf_exempt
def recommendation(request):
    print("Exec recommendation")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        userId = form.data.get("userId")

        nn = nearestNeighbor.NearestNeighbor()

        if nn.validateUserId(userId):
            recommendations = nn.getRecommendation(userId)
            #recommendations = nn.loadDebugDataframe()  # use this to avoid waiting time when dubigging
            
            recommendationDict = recommendations.to_dict(orient="records")

            template = loader.get_template('recommenderSystem/recommendation.html')
            context = {
                'data': recommendationDict,
                'userId': userId,
            }
            return HttpResponse(template.render(context))

        else:
            template = loader.get_template('recommenderSystem/index.html')
            context = {
                'errorMessage': 'This userId does not exist',
            }
            return HttpResponse(template.render(context))





