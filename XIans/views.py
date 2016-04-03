from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo :    html does not contain proper data
#           proceed in other way

IANS = "https://www.snai.it/sport"
ORIGIN = "Ians"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor


#def retrieveMLdata():
req = Request(IANS)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

string = etree.tostring(tree, pretty_print=True)

my_file = open("my_html.html", "w")
my_file.write(string)
my_file.close()