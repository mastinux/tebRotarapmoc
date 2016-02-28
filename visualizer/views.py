from django.shortcuts import render
from django.http import HttpResponse
from XMailiwLlih import views as MLviews
from XYddapRewop import views as YRviews
from retriever.models import Match


def index(request):
    #MLviews.retrieveMLdata()
    YRviews.retrieveYRdata()

    # todo : develop basic visualization
    for m in Match.objects.all():
        print m

    return HttpResponse("Surprise, motherfucker!!!")