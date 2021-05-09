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
        'userId': '0',
    }
    return HttpResponse(template.render(context))


# function used to get experienced with html forms in django
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


            #TODO: change back to loading calculated dataframe
            #recommendations = nn.getRecommendation(userId)
            recommendations = nn.loadDebugDataframe()
            
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

    # if a GET (or any other method) we'll create a blank form
    else:
        # TODO: actually not needed but maybe handle get request later
        form = NameForm()

    return render(request, 'recommenderSystem/recommendation.html', {'form': form})


# check if user entered a ID which exists in database
def validateInput(self, value: str) -> bool:
    """
    Checks if the 'value' is contained in the 'unique_ID' set.
    """
    try:
        value = int(value)
    except ValueError:
        return False
    result = int(value) in self.dataframeRatings["userId"].unique()
    return result



