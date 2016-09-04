from datetime import date
from io import StringIO
from lxml import etree
from urllib2 import Request, urlopen
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from retriever.models import Match

ORIGIN = "yddapRewop"

# CHECKED


def parse_teams(element):
    for a_element in element.getiterator("a"):
        return a_element.text.replace(" ", "").split("-")


def parse_value(element):
    for a_element in element.getiterator("a"):
        return a_element.text.replace(" ", "").replace("-", "")


def parse_tr_element(element):
    home_wins = -1
    draw = -1
    visitor = -1
    second = 0

    for td_element in element.getiterator("td"):
        if "class" in td_element.keys() and td_element.attrib['class'] == "time border":
            if second:
                home, visitor = parse_teams(td_element)
            second = 1
        if "class" in td_element.keys() and "oddWrapper-1" in td_element.attrib['class']:
            home_wins = parse_value(td_element)
        if "class" in td_element.keys() and "oddWrapper-2" in td_element.attrib['class']:
            draw = parse_value(td_element)
        if "class" in td_element.keys() and "oddWrapper-3" in td_element.attrib['class']:
            visitor_wins = parse_value(td_element)

    if home_wins and draw and visitor_wins:
        #print home, visitor
        #print home_wins, draw, visitor_wins
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


def parse_tbody_element(element):
    for tr_element in element.getiterator("tr"):
        parse_tr_element(tr_element)


def parse_table_element(element):
    for tbody_element in element.getiterator("tbody"):
        parse_tbody_element(tbody_element)


def retrieveYRdata(url):
    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    first = 1

    table_list = list()

    for table_element in tree.getiterator("table"):
        if "id" in table_element.keys() and "class" in table_element.keys() and "style" in table_element.keys():
            if not first:
                table_list.append(table_element)
            first = 0

    for table_element in table_list:
        parse_table_element(table_element)
