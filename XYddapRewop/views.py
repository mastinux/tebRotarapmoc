from django.shortcuts import render

from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime

# todo : continue surfing html
# todo : [hint] check xpath from lxml

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

MAILLIW_LLIH = "http://www.paddypower.it/scommesse-calcio/partite/serie-a"
ORIGIN = "yddapRewop"

months = dict()
months["Gen"] = 1
months["Feb"] = 2
months["Mar"] = 3
months["Apr"] = 4
months["Mag"] = 5
months["Giu"] = 6
months["Lug"] = 7
months["Ago"] = 8
months["Set"] = 9
months["Ott"] = 10
months["Nov"] = 11
months["Dic"] = 12


def parse_datetime(formatted_date, formatted_time):
    day, month = formatted_date.split(" ")
    day = int(day)
    month = months[month]
    year = datetime.today().year

    time, zone = formatted_time.split(" ")
    hours, mins = time.split(":")
    hours = int(hours)
    mins = int(mins)

    return datetime(year, month, day, hours, mins)


def parse_teams(home_vs_visitor):
    # returns a couple of teams
    values = home_vs_visitor.replace(" ", "").split()
    home = values[0]
    visitor = values[2]
    return home, visitor


#def retrieveMLdata():
req = Request(MAILLIW_LLIH)
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

fifth_level = None

for first_level_element in tree.getiterator():
    if first_level_element.tag == "div":
        if "class" in first_level_element.keys():
            if first_level_element.attrib['class'] == "page_wrapper":

                for second_level_element in first_level_element.getchildren():
                    if second_level_element.tag == "div":
                        if "id" in second_level_element.keys():
                            if second_level_element.attrib['id'] == "content":

                                for third_level_element in second_level_element.getchildren():
                                    if third_level_element.tag == "div":
                                        if "class" in third_level_element.keys():
                                            l = third_level_element.attrib['class'].split()
                                            if "main_content" in l:

                                                for fourth_level_element in third_level_element.getchildren():
                                                    if fourth_level_element.tag == "div":
                                                        if "id" in fourth_level_element.keys():
                                                            if fourth_level_element.attrib['id'] == "main":

                                                                for fifth_level_element in fourth_level_element.getchildren():
                                                                    if fifth_level_element.tag == "div":
                                                                        if "class" in fifth_level_element.keys():
                                                                            if fifth_level_element.attrib['class'] == "box":
                                                                                fifth_level = fifth_level_element

for sixth_level_element in fifth_level.getchildren():
    if sixth_level_element.tag == "div":
        if "class" in sixth_level_element.keys():
            if sixth_level_element.attrib['class'] == "fbcpn_X7":

                print "---"
                print sixth_level_element.getchildren()



