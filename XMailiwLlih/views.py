from django.shortcuts import render

from HTMLParser import HTMLParser
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime

# FIXME : problems importing Match model in this view

# TODO : define basic view for this app

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

MAILLIW_LLIH = "http://sports.williamhill.it/bet_ita/it/betting/t/321/Serie+A.html"
ORIGIN = "mailliwLlih"

# from 1 to 12
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
    # returns datetime object from formatted objects

    #print formatted_date
    day, month = formatted_date.split(" ")
    day = int(day)
    month = months[month]
    year = datetime.today().year
    #print day
    #print month
    #print year

    #print formatted_time
    time, zone = formatted_time.split(" ")
    hours, mins = time.split(":")
    hours = int(hours)
    mins = int(mins)
    #print hours, mins

    return datetime(year, month, day, hours, mins)


def parse_teams(home_vs_visitor):
    # returns a couple of teams
    values = home_vs_visitor.replace(" ", "").split()
    home = values[0]
    visitor = values[2]
    return home, visitor


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
# tree is a lxml.etree._ElementTree
tree = etree.parse(StringIO(html), parser)
#for s in [method for method in dir(tree) if callable(getattr(tree, method))]:
#    print s

for o in tree.getiterator():
    # o is a lxml.etree._Element
    if o.tag == "tr":
        tr_element = o
        #print "\n", o.tag, "\n", o.attrib
        formatted_date_ok = ""
        formatted_time_ok = ""
        home_vs_visitor_ok = ""
        home_ok = ""
        visitor_ok = ""
        home_wins_ok = -1
        draw_ok = -1
        visitor_wins_ok = -1
        for i, td_element in enumerate(tr_element.getchildren()):
            # c is a lxml.etree._Element
            if i == 0:
                #print "date"
                span_element = td_element.getchildren()[0]
                #print span_element.tag, span_element.attrib
                formatted_date_ok = span_element.text
            elif i == 1:
                #print "hour"
                span_element = td_element.getchildren()[0]
                #print span_element.tag, span_element.attrib
                formatted_time_ok = span_element.text
                #print formatted_time
            elif i == 2:
                #print "home - visitor"
                home_vs_visitor = ""
                for ii, a_element in enumerate(td_element.getchildren()):
                    for iii, span_element in enumerate(a_element.getchildren()):
                        home_vs_visitor = span_element.text
                if not home_vs_visitor:
                    break
                #print home_vs_visitor
                home_vs_visitor_ok = home_vs_visitor
            #elif i == 3:
            #    print "empty"
            elif i == 4:
                #print "home wins"
                for ii, div_element in enumerate(td_element.getchildren()):
                    for iii, divdiv_element in enumerate(div_element.getchildren()):
                        home_wins = divdiv_element.text
                        if home_wins:
                            home_wins = float(home_wins.strip())
                            #print home_wins
                            home_wins_ok = home_wins
            elif i == 5:
                #print "draw"
                for ii, div_element in enumerate(td_element.getchildren()):
                    for iii, divdiv_element in enumerate(div_element.getchildren()):
                        draw = divdiv_element.text
                        if draw:
                            draw = float(draw.strip())
                            #print draw
                            draw_ok = draw
            elif i == 6:
                #print "visitor wins"
                for ii, div_element in enumerate(td_element.getchildren()):
                    for iii, divdiv_element in enumerate(div_element.getchildren()):
                        visitor_wins = divdiv_element.text
                        if visitor_wins:
                            visitor_wins = float(visitor_wins.strip())
                            #print visitor_wins
                            visitor_wins_ok = visitor_wins
        #print formatted_date_ok, formatted_time_ok, home_vs_visitor_ok, home_wins_ok, draw_ok, visitor_wins_ok
        if home_wins_ok > 0:
            #print formatted_date_ok, formatted_time_ok, home_vs_visitor_ok, home_wins_ok, draw_ok, visitor_wins_ok
            match_datetime = parse_datetime(formatted_date_ok, formatted_time_ok)
            #print match_datetime
            home_ok, visitor_ok = parse_teams(home_vs_visitor)
            #print home_ok, "vs", visitor_ok
            print match_datetime, home_ok, "-", visitor_ok, "\t[", home_wins_ok, "/", draw_ok, "/", visitor_wins_ok, "]"

            """
            match = main_match()
            match.origin = ORIGIN
            match.datetime = formatted_date_ok
            match.home = home_ok
            match.visitor = visitor_ok
            match.price_1 = home_wins_ok
            match.price_x = draw_ok
            match.price_2 = visitor_wins_ok
            print match
            """