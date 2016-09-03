from datetime import date
from io import StringIO
from lxml import etree
from urllib2 import Request, urlopen
#from retriever.models import Match

ORIGIN = "yddapRewop"


def parse_datetime(formatted_date, formatted_time):
    date_list = formatted_date.split("-")
    year = int(date_list[0].replace("'", ""))
    month = int(date_list[1].replace("'", ""))
    day = int(date_list[2].replace("'", ""))

    time_list = formatted_time.split(":")
    hours = int(time_list[0].replace("'", ""))
    mins = int(time_list[1].replace("'", ""))

    return date(year, month, day)


def parse_teams(home_vs_visitor):
    teams = home_vs_visitor.split("-")

    home = teams[0].replace(" ", "").replace("'", "").replace(" ", "")
    visitor = teams[1].replace(" ", "").replace("'", "").replace(" ", "")

    return home, visitor


def parse_td_elements(elements):
    home = None
    home_wins = None
    draw_name = None
    draw = None
    visitor = None
    visitor_wins = None

    for e in elements:
        e.tag
        if e.attrib['class'] == "team":
            if not home:
                home = e.text
            elif not draw_name:
                draw_name = e.text
            else:
                visitor = e.text
        elif e.attrib['class'] == "price":
            for c in e.getiterator():
                if c.tag == "a":
                    if not home_wins:
                        home_wins = c.text
                    elif not draw:
                        draw = c.text
                    else:
                        visitor_wins = c.text

    print home, home_wins
    print draw
    print visitor, visitor_wins
    """
    match = Match()
    match.origin = ORIGIN
    match.datetime = date(2016, 6, 1)
    match.home = home[:-1].replace(" ", "").lower().capitalize()
    match.visitor = visitor[:-1].replace(" ", "").lower().capitalize()
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
    """


def retrieveYRdata(url):
    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    elements = list()
    new_elements = list()

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys():
            if div_element.attrib['class'] == "fb-mkt":
                new_elements.append(div_element)

    tree = None
    elements = new_elements
    new_elements = list()

    for div_element in elements:
        for table_element in div_element.getiterator("table"):
            if "class" in table_element.keys():
                new_elements.append(table_element)

    elements = new_elements
    new_elements = list()

    for table_element in elements:
        for element in table_element.getiterator():
            if element.tag == "td":
                new_elements.append(element)
        parse_td_elements(new_elements)
        new_elements = list()
