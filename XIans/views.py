from django.shortcuts import render
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime

# todo :    html does not contain proper data
#           proceed in other way

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

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

"""
parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
# print indented html code
print result
"""
"""
html2 = etree.HTML(html)
result = etree.tostring(html2, pretty_print=True, method="html")
# print indented html code
print result
"""
"""
parser = etree.HTMLParser(target=EchoTarget())
# scroll html while printing data by EchoTarget()
result = etree.HTML(html, parser)
"""
"""
parser = etree.HTMLParser(target=etree.TreeBuilder())
# result is the root of html, it contains head and body
result = etree.HTML(html, parser)
#print type(result) # <type 'lxml.etree._Element'>
"""

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

string = etree.tostring(tree, pretty_print=True)

my_file = open("my_html.txt", "w")
my_file.write(string)
my_file.close()

"""
for o in tree.getiterator():
    print "\n", o.tag
    print o.attrib
"""