from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
import execjs
from webbrowser import open as webbrowser_open
import selenium.webdriver as webdriver
from datetime import date
from retriever.models import Match
from pyvirtualdisplay import Display

ORIGIN = "ians"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(element):
    for a_element in element.getiterator("a"):
        teams = (a_element.text).replace(" ", "").replace("\n", "").split("-")
        home = teams[0]
        if home == "NIrlanda":
            home = "Irlandadelnord"
        visitor = teams[1]
        if visitor == "NIrlanda":
            visitor = "Irlandadelnord"
        return home.lower().capitalize(), visitor.lower().capitalize()


def parse_tr_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for td_element in element.getiterator("td"):
        if not home:
            home, visitor = parse_teams(td_element)
        elif not home_wins:
            home_wins = td_element.text.replace(" ", "").replace("\n", "").replace(",", ".")
        elif not draw:
            draw = td_element.text.replace(" ", "").replace("\n", "").replace(",", ".")
        else:
            visitor_wins = td_element.text.replace(" ", "").replace("\n", "").replace(",", ".")

    match = Match()
    match.origin = ORIGIN
    match.datetime = date(2016, 6, 1)
    match.home = home.replace(" ", "")
    match.visitor = visitor.replace(" ", "")
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


def retrieveIdata(url):
    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    print html

    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "id" in div_element.keys() and div_element.attrib["id"] == "piuGiocate_CALCIO":
            my_div = div_element
            tree = None
            break

    for tr_element in my_div.getiterator("tr"):
        if "class" in tr_element.keys():
            parse_tr_element(tr_element)
    """