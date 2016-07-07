from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

ORIGIN = "niwb"


def parse_td_element(element):
    a = None
    b = None

    for span_element in element.getiterator("span"):
        if "class" in span_element.keys() and span_element.attrib["class"] == "option-name":
            a = span_element.text.replace(" ", "")
        if "class" in span_element.keys() and span_element.attrib["class"] == "odds":
            b = span_element.text

    return a, b


def parse_tr_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for td_element in element.getiterator("td"):
        if not home:
            home, home_wins = parse_td_element(td_element)
        elif not draw:
            draw, draw = parse_td_element(td_element)
        elif not visitor:
            visitor, visitor_wins = parse_td_element(td_element)

            match = Match()
            match.origin = ORIGIN
            match.datetime = date(2016, 6, 1)
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

            home = None
            visitor = None
            home_wins = None
            draw = None
            visitor_wins = None


def retrieveNdata(url):
    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for tr_element in tree.getiterator("tr"):
        if "class" in tr_element.keys() and tr_element.attrib["class"] == "col3 three-way":
            parse_tr_element(tr_element)
