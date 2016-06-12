from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

RETTEB = "https://www.lottomatica.it/scommesse/avvenimenti/calcio/europa/campeuropei.html"
ORIGIN = "retteb"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor


#def retrieveMLdata():
req = Request(RETTEB)
response = urlopen(req)
html = response.read()

parser = etree.HTMLParser()
tree = etree.parse(StringIO(unicode(html, "utf-8")), parser)


for element in tree.getiterator("div"):
    if "class" in element.keys() and element.attrib["class"] == "ng-scope":
        print element.tag, element.attrib

# FIXME: can't get data