from lxml import etree
from io import StringIO
from datetime import date
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from datetime import date
from time import sleep
from retriever.models import Match

# CHECKED

ORIGIN = "TenTeb"


def parse_div_element(element):
    home = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for span_element in element.getiterator("span"):
        string = span_element.text
        if not home:
            home = string
        elif not visitor:
            visitor = string
        elif not home_wins:
            home_wins = string
        elif not draw:
            draw = string
        elif not visitor_wins:
            visitor_wins = string

    home = home.replace("AS ", "").replace("AC ", "")
    visitor = visitor.replace("AS ", "").replace("AC ", "")

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


def retrieveTTdata(url):
    print "processing tenTeb ..."

    display = Display(visible=0, size=(1024, 1024))
    display.start()

    # driver = webdriver.Firefox()

    # http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(5)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "types_bg":
            tree = div_element

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "bets ml":
            parse_div_element(div_element)
