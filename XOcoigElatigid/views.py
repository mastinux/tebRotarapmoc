from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match


ORIGIN = "OcoigElatigid"


def parse_value(v):
    if ("+" in v) or ("-" in v):
        v = float(v)
        if v > 0:
            v = v / 100 + 1
        else:
            v = 100 / (-v) + 1
    elif "/" in v:
        a, b = v.split("/")
        v = float(a) / float(b)
        v += 1
    else:
        v = float(v)

    return round(v, 2)


def parse_td_element(element):
    a = None
    b = None

    for div_element in element.getiterator("div"):
        if "class" in div_element.keys() and "mb-option-button__option-name" in div_element.attrib["class"]:
            a = div_element.text
        if "class" in div_element.keys() and "mb-option-button__option-odds" in div_element.attrib["class"]:
            b = div_element.text

    return a, b


def parse_table_element(element):
    home = None
    home_wins = None
    draw_string = None
    draw = None
    visitor = None
    visitor_wins = None

    for td_element in element.getiterator("td"):
        if "title" in td_element.keys():
            if not home:
                home, home_wins = parse_td_element(td_element)
            elif not draw:
                draw_string, draw = parse_td_element(td_element)
            elif not visitor:
                visitor, visitor_wins = parse_td_element(td_element)

    match_datetime = date(2016, 6, 1)

    match = Match()
    match.origin = ORIGIN
    match.datetime = match_datetime
    match.home = home.lower().capitalize()
    match.visitor = visitor.lower().capitalize()
    match.price_1 = parse_value(home_wins)
    match.price_x = parse_value(draw)
    match.price_2 = parse_value(visitor_wins)

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


def retrieveOEdata(url):
    print 'processing ocoigElatigid'

    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    i = 0

    for table_element in tree.getiterator("table"):
        if "class" in table_element.keys() and "marketboard-event-without-header__markets-list" == table_element.attrib["class"]:
            parse_table_element(table_element)
            i += 1
            if i >= 10:
                break

