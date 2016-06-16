from django.shortcuts import render
from django.http import HttpResponse
from XMailiwLlih import views as MLviews
from XYddapRewop import views as YRviews
from XIans import views as Iviews
from retriever.models import Match
from datetime import datetime

PAYMENT = 100


def present(datum, data):
    for d in data:
        if d["home"] == datum["home"] and d["visitor"] == datum["visitor"] and d["datetime"] == datum["datetime"]:
            return True
    return False


def index(request):
    context = {}
    data = list()
    today = datetime.now()
    
    for m in Match.objects.all():
        Match.delete(m)

    MLviews.retrieveMLdata()
    YRviews.retrieveYRdata()

    matches = Match.objects.all()

    homes = [m.home for m in matches]
    homes_set = set(list(homes))

    #visitors = [m.visitor for m in matches]
    #datetimes = [m.datetime for m in matches]

    #for i in range(0, len(homes)):
    for home in homes_set:
        """
        local = matches.filter(home=homes[i]
                               , visitor=visitors[i]
                               #, datetime=datetimes[i]
                               )
        """
        local = matches.filter(home=home)
	visitor = local[0].visitor
	local = matches.filter(home=home, visitor=visitor)
        #print local
        if len(local) > 1:
            #visitor = local[0].visitor
            max_1 = local[0].price_1
            match_1_max = 0
            max_x = local[0].price_x
            match_x_max = 0
            max_2 = local[0].price_2
            match_2_max = 0
            for idx, local_match in enumerate(local):
                if local_match.price_1 > max_1:
                    max_1 = local_match.price_1
                    match_1_max = idx
                if local_match.price_x > max_x:
                    max_x = local_match.price_x
                    match_x_max = idx
                if local_match.price_2 > max_2:
                    max_2 = local_match.price_2
                    match_2_max = idx

            cost_1 = PAYMENT / max_1
            cost_x = PAYMENT / max_x
            cost_2 = PAYMENT / max_2
            total_cost = cost_1 + cost_x + cost_2

            datum = {'home': home, 'visitor': visitor, 'datetime': datetime.now(), 'matches': local,
                     'max_1': max_1, 'max_x': max_x, 'max_2': max_2, 'match_1_max': match_1_max,
                     'match_x_max': match_x_max, 'match_2_max': match_2_max, 'cost_1': cost_1, 'cost_x': cost_x,
                     'cost_2': cost_2, 'total_cost': total_cost}
            if not present(datum, data):
                data.append(datum)

    context['data'] = data
    context['payment'] = PAYMENT

    return render(request, 'index.html', context)


def index_2(request):
    return render(request, 'index_2.html')


def index_3(request):
    context = {}

    matches = Match.objects.all().order_by("home", "visitor")

    context["matches"] = matches

    return render(request, 'index_3.html', context)
