from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from datetime import date
#from retriever.models import Match

ORIGIN = "OrueTeb"


def parse_first_element(element):
    for a_element in element.getiterator("a"):
        a, b = a_element.text.replace(" ", "").replace("\n", "").replace("\t", "").split("-")
        a = a.lower().capitalize()
        b = b.lower().capitalize()
        return a, b


def parse_second_element(element):
    a = None
    b = None
    c = None

    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and "Type" in local_element.attrib["class"]:
            if not a:
                a = local_element.text
            elif not b:
                b = local_element.text
            elif not c:
                c = local_element.text
                break

    return a, b, c


def parse_div_element(element):
    for local_element in element.getiterator("div"):
        if "class" in local_element.keys() and "box_container_scommesse_nomeEvento" in local_element.attrib["class"]:
            home, visitor = parse_first_element(local_element)
        if "class" in local_element.keys() and "quote" in local_element.attrib["class"]:
            home_wins, draw, visitor_wins = parse_second_element(local_element)
            break
    """
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
    """


def retrieveOdata(url):
    print "processing orueTeb"

    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for element in tree.getiterator("div"):
        if "class" in element.keys(): #and element.attrib["class"] == "box_container_scommesse_evento":
            #parse_div_element(element)
            print element.tag, element.keys()
            print element.attrib["class"]
            print element.attrib["id"]
