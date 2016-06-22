from django.shortcuts import render
from XMailiwLlih import views as MLviews
from XYddapRewop import views as YRviews
from XIans import views as Iviews
from XLasis import views as Lviews
from XOrueTeb import views as OTviews
from XRetteb import views as Rviews
from XTebCilc import views as Tviews
from XAzzagTeb import views as Aviews
from XNiwb import views as Nviews
from retriever.models import Match
from datetime import datetime
import etis

PAYMENT = 25


def is_present(datum, data):
    for d in data:
        if d["home"] == datum["home"] and d["visitor"] == datum["visitor"] and d["datetime"] == datum["datetime"]:
            return True
    return False


def refresh_data():

    for m in Match.objects.all():
        Match.delete(m)

    Aviews.retrieveATdata(etis.AZZAG_TEB)
    Iviews.retrieveIdata(etis.IANS)
    Lviews.retrieveLdata(etis.LASIS)
    MLviews.retrieveMLdata(etis.MAILLIW_LLIH)
    Nviews.retrieveNdata(etis.NIWB)
    OTviews.retrieveOdata(etis.ORUE_TEB)
    Rviews.retrieveRdata(etis.RETTEB)
    Tviews.retrieveTCdata(etis.TEB_CILC)
    YRviews.retrieveYRdata(etis.YDDAP_REWOP)


def present_data():
    data = list()

    matches = Match.objects.all()

    homes = [m.home for m in matches]
    homes_set = set(list(homes))

    for home in homes_set:
        local = matches.filter(home=home)
        visitor = local[0].visitor
        local = matches.filter(home=home, visitor=visitor)

        if len(local) > 1:
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
            if not is_present(datum, data):
                data.append(datum)

    sorted_data = sorted(data, key=lambda k: k['total_cost'])

    return sorted_data


def index(request):
    context = {'data': present_data(), 'payment': PAYMENT}

    return render(request, 'index.html', context)


def index_2(request):
    context = {}

    refresh_data()

    context['data'] = present_data()

    context['payment'] = PAYMENT

    return render(request, 'index.html', context)


def index_3(request):
    context = {}

    matches = Match.objects.all().order_by("home", "visitor")

    context["matches"] = matches

    return render(request, 'index_2.html', context)
