from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

ORIGIN = "TebCilc"

# CHECKED


def parse_first_element(element):
    for a_element in element.getiterator("a"):
        a, b = a_element.text.replace(" ", "").split("-")
        a = a.lower().capitalize()
        b = b.lower().capitalize()
        return a, b


def parse_second_element(element):
    a = None
    b = None
    c = None

    for span_element in element.getiterator("span"):
        if not a:
            a = span_element.text.replace(",", ".")
        elif not b:
            b = span_element.text.replace(",", ".")
        elif not c:
            c = span_element.text.replace(",", ".")
            return a, b, c


def parse_div_element(element):
    for div_element in element.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "match-name":
            home, visitor = parse_first_element(div_element)
        if "class" in div_element.keys() and div_element.attrib["class"] == "match-odds":
            home_wins, draw, visitor_wins = parse_second_element(div_element)

            match = Match()
            match.origin = ORIGIN
            match.datetime = date(2016, 6, 1)
            match.home = home
            match.visitor = visitor
            match.price_1 = float(home_wins)
            match.price_x = float(draw)
            match.price_2 = float(visitor_wins)

            tmp = match.is_stored()
            if tmp:
                tmp = tmp.first()
                if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
                    print '\nupdate\t', tmp
                    tmp.delete()
                    print "to\t", match
                    match.save()
                else:
                    print match, "already stored"
            else:
                print "saving", match
                match.save()


def retrieveTCdata(url):
    print 'processing tebCilc'

    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and "match-entry" in div_element.attrib["class"]:
            parse_div_element(div_element)
