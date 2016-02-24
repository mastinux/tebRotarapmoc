from django.shortcuts import render
from django.http import HttpResponse
from XMailiwLlih import views


def index(request):
    views.retrieveMLdata()
    return HttpResponse("Surprise, motherfucker!!!")