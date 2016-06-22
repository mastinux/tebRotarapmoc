from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
import selenium.webdriver as webdriver
from retriever.models import Match
from datetime import date

ORIGIN = "lasis"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_first_element(element):
    for a_element in element.getiterator("a"):
        a, b = a_element.text.replace(" ", "").split("-")
        break

    a = a.lower().capitalize()
    b = b.lower().capitalize()

    if a == "Rep.ceca":
        a = "Repubblicaceca"
    if b == "Rep.ceca":
        b = "Repubblicaceca"

    return a, b


def parse_second_element(element):
    a = None
    b = None
    c = None

    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and "quota-label" in local_element.attrib["class"]:
            if not a:
                a = local_element.text
            elif not b:
                b = local_element.text
            else:
                c = local_element.text
                break

    return a, b, c


def parse_div_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and\
                ((local_element.attrib["class"] == "event") or (local_element.attrib["class"] == "event odd")):
            event_div = local_element
            break

    for local_element in event_div.getiterator("div"):
        if "class" in local_element.keys() and local_element.attrib["class"] == "detail":
            home, visitor = parse_first_element(local_element)
        if "class" in local_element.keys() and local_element.attrib["class"] == "quote":
            home_wins, draw, visitor_wins = parse_second_element(local_element)

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


def retrieveLdata(url):
    """
    PDF_NAME = "document.pdf"

    response = urlopen(PDF_LASIS)
    f = open(PDF_NAME, 'w')
    f.write(response.read())
    f.close()
    """

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    """
    f = open("page.html", "w")
    f.write(html)
    f.close()
    """

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "partitasingola"\
                and "style" in div_element.keys() and div_element.attrib["style"] == "display: block;":
            parse_div_element(div_element)
