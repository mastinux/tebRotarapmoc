from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

# CHECKED

ORIGIN = "Ocipit"


def parse_div_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for div_element in element.getiterator("div"):
        if "class" in div_element.keys() and "t_cell" in div_element.attrib["class"]:
            tmp = div_element.text.replace("\t", "").replace("\n", "")
            if not home:
                home = tmp
            elif not visitor:
                visitor = tmp
        if "class" in div_element.keys() and "qbut" in div_element.attrib["class"]:
            tmp = div_element.text.replace(",", ".")
            if not home_wins:
                home_wins = tmp
            elif not draw:
                draw = tmp
            elif not visitor_wins:
                visitor_wins = tmp

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


def retrieveOdata(url):
    print 'processing ocipit'
    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and "e_active t_row" in div_element.attrib["class"]:
            parse_div_element(div_element)
