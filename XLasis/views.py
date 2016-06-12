from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo :    html does not contain proper data
#           proceed in other way

LASIS = "http://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=21&fil=0"
PDF_LASIS = "http://landing.sisal.it/volantini/Scommesse_Sport/Quote/calcio%20base%20per%20data.pdf"
ORIGIN = "lasis"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor

#def retrieveYRdata():
"""
PDF_NAME = "document.pdf"

response = urlopen(PDF_LASIS)
f = open(PDF_NAME, 'w')
f.write(response.read())
f.close()
"""
req = Request(LASIS)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

for element in tree.getiterator("div"):
    if "class" in element.attrib and element.attrib["class"] == "event":
        print element.tag, element.attrib

# FIXME: can't access div {'class': 'event odd'}