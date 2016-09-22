from lxml import etree
from io import StringIO
from selenium import webdriver
from pyvirtualdisplay import Display
from retriever.models import Match
from datetime import date

ORIGIN = "Retteb"


def parse_teams(element):
    for first in element.getiterator("a"):
        for second in first.getiterator("strong"):
            a, b = second.text.lower().replace(" ", "").split("-")

    a = a.capitalize()
    b = b.capitalize()

    return a, b


def parse_second(element):
    for a_element in element.getiterator("a"):
        return a_element.text


def parse_tr_element(element):
    home_wins = None
    draw = None
    visitor_wins = None

    for td_element in element.getiterator("td"):
        if "colspan" in td_element.keys():
            home, visitor = parse_teams(td_element)

        if "class" in td_element.keys() and "col-bet ng-scope" in td_element.attrib["class"]:
            if not home_wins:
                home_wins = parse_second(td_element)
            elif not draw:
                draw = parse_second(td_element)
            elif not visitor_wins:
                visitor_wins = parse_second(td_element)

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

                home_wins = None
                draw = None
                visitor_wins = None


def retrieveRdata(url):
    print 'processing retteb'
    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for element in tree.getiterator("tr"):
        if "class" in element.keys() and element.attrib["class"] == "ng-scope"\
                and "ng-repeat" in element.keys() and "eventM" in element.attrib["ng-repeat"]:
            parse_tr_element(element)
