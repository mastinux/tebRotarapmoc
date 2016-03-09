from django.shortcuts import render
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

RETTEB = "https://www.lottomatica.it/scommesse/avvenimenti/calcio/italia/seriea"
ORIGIN = "retteb"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor


#def retrieveMLdata():
req = Request(RETTEB)
response = urlopen(req)
html = response.read()

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
tree = etree.parse(StringIO(unicode(html, "utf-8")), parser)

first_level_element = None
for o in tree.getiterator():
    if o.tag == "div" and "class" in o.keys():
        if o.attrib['class'] == "super-wrapper":
            first_level_element = o
            tree = None
            break

for o in first_level_element.getchildren():
    if o.tag == "section":
        second_level_element = o
        first_level_element = None
        break

for o in second_level_element.getchildren():
    if o.tag == "div":
        third_level_element = o
        second_level_element = None
        break

for i, o in enumerate(third_level_element.getchildren()):
    if o.tag == "div" and i == 0:
        fourth_level_element = o
        third_level_element = None
        break

for o in fourth_level_element.getchildren():
    if o.tag == "div":
        fifth_level_element = o
        fourth_level_element = None
        break

for i, o in enumerate(fifth_level_element.getchildren()):
    if o.tag == "div" and i == 1:
        sixth_level_element = o
        fifth_level_element = None
        break

for o in sixth_level_element.getchildren():
    if o.tag == "div":
        seventh_level_element = o
        sixth_level_element = None
        break

for i, o in enumerate(seventh_level_element.getchildren()):
    if o.tag == "div" and i == 1:
        eighth_level_element = o
        seventh_level_element = None
        break

for i, o in enumerate(eighth_level_element.getchildren()):
    if o.tag == "div" and i == 1:
        ninth_level_element = o
        eighth_level_element = None
        break

for o in ninth_level_element.getchildren():
    if o.tag == "div":
        tenth_level_element = o
        ninth_level_element = None
        break

for o in tenth_level_element.getchildren():
    # todo : no more children found
    print o.tag
