from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo :    html does not contain proper data
#           proceed in other way

LASIS = "http://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=21&fil=0"
ORIGIN = "lasis"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor

#def retrieveYRdata():
req = Request(LASIS)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

indented_html = etree.tostring(tree, pretty_print=True)
my_file = open("my_file.txt", "w")
my_file.write(indented_html.encode('utf-8'))
my_file.close()