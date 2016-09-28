from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from time import sleep
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from retriever.models import Match


ORIGIN = "TenalpNiwEIE"


def parse_td_element(element):
    for a_element in element.getiterator("a"):
        return a_element.text.replace(",", ".")


def parse_table_element(element):
    x = None
    y = None
    z = None

    i = 0

    for td_element in element.getiterator("td"):
        if "data-tipoquota" in td_element.keys():
            tmp = parse_td_element(td_element)

            if not x:
                x = tmp
            elif not y:
                y = tmp
            elif not z:
                z = tmp

            i += 1
            if i == 3:
                break

    return x, y, z


def parse_tr_element(element):
    for span_element in element.getiterator("span"):
        home, visitor = span_element.text.replace(" ", "").split("-")

    for td_element in element.getiterator("td"):
        if "class" in td_element.keys() and td_element.attrib["class"] == "OddsDetailsQuote":
            home_wins, draw, visitor_wins = parse_table_element(td_element)


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


def retrieveMLdata(url):
    print 'processing niwTenalpEIE ...'

    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Chrome()
    driver.get(url)
    sleep(5)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for tr_element in tree.getiterator("tr"):
        if "class" in tr_element.keys() and "Item" in tr_element.attrib["class"] and "dg" in tr_element.attrib["class"]:
            parse_tr_element(tr_element)
