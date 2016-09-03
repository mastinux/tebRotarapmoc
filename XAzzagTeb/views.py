from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

# CHECKED

ORIGIN = "azzagTeb"


def parse_td_element(element):
    a = None
    b = None

    for span_element in element.getiterator("span"):
        if "class" in span_element.keys() and "seln-name" in span_element.attrib["class"]:
            a = span_element.text
        if "class" in span_element.keys() and "price dec" in span_element.attrib["class"]:
            b = span_element.text

    return a, b


def parse_tr_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for td_element in element.getiterator("td"):
        if "class" in td_element.keys() and "seln" in td_element.attrib["class"]:
            if not home:
                home, home_wins = parse_td_element(td_element)
            elif not draw:
                draw, draw = parse_td_element(td_element)
            elif not visitor:
                visitor, visitor_wins = parse_td_element(td_element)

    match_datetime = date(2016, 6, 1)

    match = Match()
    match.origin = ORIGIN
    match.datetime = match_datetime
    match.home = home.lower().capitalize()
    match.visitor = visitor.lower().capitalize()
    match.price_1 = float(home_wins)
    match.price_x = float(draw)
    match.price_2 = float(visitor_wins)

    tmp = match.is_stored()
    if tmp:
        tmp = tmp.first()
        if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
            print "\nupdate\t", tmp
            tmp.delete()
            print "to\t", match
            match.save()
        else:
            print match, "already stored"
    else:
        print "saving", match
        match.save()


def retrieveATdata(url):
    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for tr_element in tree.getiterator("tr"):
        if "class" in tr_element.keys() and "mkt" in tr_element.attrib["class"]:
            parse_tr_element(tr_element)
