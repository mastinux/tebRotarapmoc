from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
import selenium.webdriver as webdriver
from datetime import date
from retriever.models import Match

ORUE_TEB = "http://web.eurobet.it/webeb/scommesse-sportive?action=showMeeting" \
           "&disciplineCode=1" \
           "&meetingCode=42" \
           "&betTypesParam=-1" \
           "&betTypeGroupSel=-1" \
           "&showSplash=0" \
           "&partid=nuFYWiDMdCzhFJ7n09KR-WNd7ZgqdRLk" \
           "&maagid=122" \
           "&amc_cid=ps_Adwords_Europei2016_Scommesse_null" \
           "&url=http://web.eurobet.it/webeb/scommesse-sportive%3Faction%3DshowMeeting%26disciplineCode%3D1%26meetingCode%3D42%26betTypesParam%3D-1%26betTypeGroupSel%3D-1%26showSplash%3D0" \
           "&payload=%2Bscommesse%20%2Beuropei_b_100087147477_c" \
           "&gclid=CIDAho7utM0CFcWVGwod-9wILQ"
ORIGIN = "orueTeb"


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


def retrieveOdata():
    url = ORUE_TEB

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source

    driver.quit()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for element in tree.getiterator("div"):
        if "class" in element.keys() and element.attrib["class"] == "box_container_scommesse_evento":
            parse_div_element(element)
