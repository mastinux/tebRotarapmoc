from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

# CHECKED

ORIGIN = "TebRiaf"


def parse_first_element(element):
    print element.tag


def parse_second_element(element):
    print element.tag


def parse_li_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for span_element in element.getiterator("span"):
        if "class" in span_element.keys() and "team-name" in span_element.attrib["class"]:
            string = span_element.text.replace(" ", "").replace("\n", "")
            if not home:
                home = string
            elif not visitor:
                visitor = string
        if "class" in span_element.keys() and "ui-runner-price" in span_element.attrib["class"]:
            string = span_element.text.replace(" ", "").replace("\n", "")
            if not home_wins:
                home_wins = string
            elif not draw:
                draw = string
            elif not visitor_wins:
                visitor_wins = string

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


def retrieveTRdata(url):
    print 'processing TebRiaf'

    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    elements = list()

    for li_element in tree.getiterator("li"):
        if "class" in li_element.keys() and "line" in li_element.attrib["class"]:
            elements.append(li_element)

    for element in elements:
        parse_li_element(element)
