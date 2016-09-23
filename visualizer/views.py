from django.shortcuts import render
from retriever.models import Match
from datetime import datetime
from time import sleep
from math import ceil
from . import etis

from XAzzagTeb import views as ATviews
from XIans import views as Iviews
from XLasis import views as Lviews
from XMailiwLlih import views as MLviews
from XNiwb import views as Nviews
from XOcipit import views as Oviews
from XOcoigElatigid import views as OEviews
from XRetteb import views as Rviews
from XTebCilc import views as TCviews
from XTebRiaf import views as TRviews
from XTenTeb import views as TTviews
from XYddapRewop import views as YRviews

PAYMENT = 100


def is_present(datum, data):
    for d in data:
        if d["home"] == datum["home"] and d["visitor"] == datum["visitor"] and d["datetime"] == datum["datetime"]:
            return True
    return False


def refresh_data():

    for m in Match.objects.all():
        Match.delete(m)

    sleep(3)
    Rviews.retrieveRdata(etis.RETTEB)
    sleep(1)
    ATviews.retrieveATdata(etis.AZZAG_TEB)
    sleep(3)
    Iviews.retrieveIdata(etis.IANS)
    sleep(3)
    Lviews.retrieveLdata(etis.LASIS)
    sleep(1)
    MLviews.retrieveMLdata(etis.MAILLIW_LLIH)
    sleep(3)
    Nviews.retrieveNdata(etis.NIWB)
    sleep(1)
    Oviews.retrieveOdata(etis.OCIPIT)
    sleep(1)
    OEviews.retrieveOEdata(etis.OCOIG_ELATIGID)
    sleep(1)
    TCviews.retrieveTCdata(etis.TEB_CILC)
    sleep(1)
    TRviews.retrieveTRdata(etis.TEB_RIAF)
    sleep(3)
    TTviews.retrieveTTdata(etis.TEN_TEB)
    sleep(3)
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
            cost_1 = ceil(cost_1)

            cost_x = PAYMENT / max_x
            cost_x = ceil(cost_x)

            cost_2 = PAYMENT / max_2
            cost_2 = ceil(cost_2)

            total_cost = cost_1 + cost_x + cost_2

            gain_1 = max_1 * cost_1
            gain_x = max_x * cost_x
            gain_2 = max_2 * cost_2

            min_gain = min([gain_1, gain_x, gain_2])

            if total_cost < min_gain:
                # TODO: send email
                print ">>> strike!!! <<<"

            datum = {'home': home, 'visitor': visitor, 'datetime': datetime.now(), 'matches': local,
                     'max_1': max_1, 'max_x': max_x, 'max_2': max_2, 'match_1_max': match_1_max,
                     'match_x_max': match_x_max, 'match_2_max': match_2_max, 'cost_1': cost_1, 'cost_x': cost_x,
                     'cost_2': cost_2, 'gain_1': gain_1, 'gain_x': gain_x, 'gain_2': gain_2, 'min_gain': min_gain,
                     'total_cost': total_cost}
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


def scheduled_refresh():
    refresh_data()
