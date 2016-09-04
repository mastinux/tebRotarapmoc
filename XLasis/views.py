from lxml import etree
from io import StringIO
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from retriever.models import Match
from datetime import date

ORIGIN = "lasis"

# CHECKED


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_first_elements(elements):
    return elements.replace(" ", "").split("-")


def parse_second_elements(element):
    a = None
    b = None
    c = None

    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and "quota-label" in local_element.attrib['class']:
            if not a:
                a = local_element.text
            elif not b:
                b = local_element.text
            else:
                c = local_element.text
                break

    return a, b, c


def parse_event_odd_div(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and local_element.attrib["class"] == "detail":
            for a_element in local_element.getiterator("a"):
                home, visitor = parse_first_elements(a_element.text)
        if "class" in local_element.keys() and local_element.attrib['class'] == "quote":
            home_wins, draw, visitor_wins = parse_second_elements(local_element)

    if home and visitor:
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


def parse_div_element(element):
    for local_element in element.getiterator("div"):
        if "class" in local_element.keys()\
                and (local_element.attrib["class"] == "event" or local_element.attrib["class"] == "event odd"):
            parse_event_odd_div(local_element)


def retrieveLdata(url):
    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "partitasingola"\
                and "id" in div_element.keys():
            parse_div_element(div_element)
