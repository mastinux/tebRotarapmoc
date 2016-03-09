from django.shortcuts import render
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime
from retriever.models import Match

# todo : manage live scoring

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

MAILLIW_LLIH = "http://sports.williamhill.it/bet_ita/it/betting/t/321/Serie+A.html"
ORIGIN = "mailliwLlih"

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


def parse_datetime(formatted_date, formatted_time, home, visitor):
    """
    if formatted_date.find("gg"):
        today = datetime.now()
        day = today.day
        month = today.month
        year = today.year
    else:
        day, month = formatted_date.split(" ")
        day = int(day)
        month = months[month]
        year = datetime.today().year
    """
    day, month = formatted_date.split(" ")
    day = int(day)
    month = months[month]
    year = datetime.today().year
    """
    if "min" in formatted_time:
        last_record = Match.get_last_match_stored(ORIGIN, datetime(year, month, day+1, 0, 0, 0), home, visitor)
        hours = last_record.datetime.hour
        mins = last_record.datetime.minute
    else:
        time, zone = formatted_time.split(" ")
        hours, mins = time.split(":")
        hours = int(hours)
        mins = int(mins)
    """
    time, zone = formatted_time.split(" ")
    hours, mins = time.split(":")
    hours = int(hours)
    mins = int(mins)

    return datetime(year, month, day, hours, mins)


def parse_teams(home_vs_visitor):
    values = home_vs_visitor.replace(" ", "").split()
    home = values[0]
    visitor = values[2]
    return home, visitor


def retrieveMLdata():
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
    parsed_event = 0
    for o in tree.getiterator():
        if o.tag == "tr" and parsed_event < 10:
            tr_element = o
            formatted_date_ok = ""
            formatted_time_ok = ""
            home_wins_ok = -1
            draw_ok = -1
            visitor_wins_ok = -1
            for i, td_element in enumerate(tr_element.getchildren()):
                if i == 0:
                    span_element = td_element.getchildren()[0]
                    formatted_date_ok = span_element.text
                elif i == 1:
                    span_element = td_element.getchildren()[0]
                    formatted_time_ok = span_element.text
                elif i == 2:
                    home_vs_visitor = ""
                    for ii, a_element in enumerate(td_element.getchildren()):
                        for iii, span_element in enumerate(a_element.getchildren()):
                            home_vs_visitor = span_element.text
                    if not home_vs_visitor:
                        break
                    home_vs_visitor_ok = home_vs_visitor
                elif i == 4:
                    for ii, div_element in enumerate(td_element.getchildren()):
                        for iii, divdiv_element in enumerate(div_element.getchildren()):
                            home_wins = divdiv_element.text
                            if home_wins:
                                home_wins = float(home_wins.strip())
                                home_wins_ok = home_wins
                elif i == 5:
                    for ii, div_element in enumerate(td_element.getchildren()):
                        for iii, divdiv_element in enumerate(div_element.getchildren()):
                            draw = divdiv_element.text
                            if draw:
                                draw = float(draw.strip())
                                draw_ok = draw
                elif i == 6:
                    for ii, div_element in enumerate(td_element.getchildren()):
                        for iii, divdiv_element in enumerate(div_element.getchildren()):
                            visitor_wins = divdiv_element.text
                            if visitor_wins:
                                visitor_wins = float(visitor_wins.strip())
                                visitor_wins_ok = visitor_wins

            if home_wins_ok > 0 and (not ("-" in formatted_time_ok)):
                #print formatted_date_ok, formatted_time_ok, home_vs_visitor_ok, home_wins_ok, draw_ok, visitor_wins_ok
                home_ok, visitor_ok = parse_teams(home_vs_visitor)
                #print home_ok, visitor_ok

                match_datetime = parse_datetime(formatted_date_ok, formatted_time_ok, home_ok, visitor_ok)
                #print "proper datetime:", match_datetime

                #print match_datetime, "\n", home_ok, "-", visitor_ok, \
                #    "\t[", home_wins_ok, "/", draw_ok, "/", visitor_wins_ok, "]"
                match = Match()
                match.origin = ORIGIN
                match.datetime = match_datetime
                match.home = home_ok
                match.visitor = visitor_ok
                match.price_1 = home_wins_ok
                match.price_x = draw_ok
                match.price_2 = visitor_wins_ok

                tmp = match.is_stored()
                if tmp:
                    tmp = tmp.first()
                    if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
                        print "\nupdate\t", match
                        tmp.price_1 = match.price_1
                        tmp.price_x = match.price_x
                        tmp.price_2 = match.price_2
                        tmp.update()
                        print "to\t", tmp
                    else:
                        print tmp, "already stored"
                else:
                    print "saving", match
                    match.save()
                parsed_event += 1