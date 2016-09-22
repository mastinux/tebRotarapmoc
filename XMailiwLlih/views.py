from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
from retriever.models import Match

# CHECKED

ORIGIN = "MailliwLlih"

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
    year = date.today().year
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

    return date(year, month, day)


def parse_teams(home_vs_visitor):
    values = home_vs_visitor.replace(" ", "").split()
    home = values[0]
    visitor = values[2]
    return home, visitor


def retrieveMLdata(url):
    print 'processing mailliwLlih'
    req = Request(url)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

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

                #match_datetime = parse_datetime(formatted_date_ok, formatted_time_ok, home_ok, visitor_ok)
                match_datetime = date(2016, 6, 1)
                #print "proper datetime:", match_datetime

                #print match_datetime, "\n", home_ok, "-", visitor_ok, \
                #    "\t[", home_wins_ok, "/", draw_ok, "/", visitor_wins_ok, "]"

                match = Match()
                match.origin = ORIGIN
                match.datetime = match_datetime
                match.home = home_ok.lower().capitalize()
                match.visitor = visitor_ok.lower().capitalize()
                match.price_1 = home_wins_ok
                match.price_x = draw_ok
                match.price_2 = visitor_wins_ok

                tmp = match.is_stored()
                if tmp:
                    tmp = tmp.first()
                    if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
                        print "\nupdate\t", tmp
                        tmp.delete()
                        print "to\t", match
                        match.save()
                    else:
                        print match, "already stored"
                else:
                    print "saving", match
                    match.save()
                parsed_event += 1
