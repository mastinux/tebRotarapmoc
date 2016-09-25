from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
from retriever.models import Match

# CHECKED

ORIGIN = "Niwb"


def parse_div_element(element):
    home = None
    draw_string = None
    visitor = None
    home_wins = None
    draw = None
    visitor_wins = None

    for div_element in element.getiterator("div"):
        if "class" in div_element.keys() and "mb-option-button__option" in div_element.attrib["class"]:
            if not home:
                home = div_element.text
            elif not home_wins:
                home_wins = div_element.text
            elif not draw_string:
                draw_string = div_element.text
            elif not draw:
                draw = div_element.text
            elif not visitor:
                visitor = div_element.text
            elif not visitor_wins:
                visitor_wins = div_element.text

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


def retrieveNdata(url):
    print "processing niwb ..."

    display = Display(visible=0, size=(1024, 1024))
    display.start()

    # driver = webdriver.Firefox()

    # http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    #print html

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    i = 0

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys() and div_element.attrib["class"] == "marketboard-event-without-header__markets-container":
            parse_div_element(div_element)
            i += 1
        if i >= 10:
            break
