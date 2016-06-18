from datetime import date
from io import StringIO
from lxml import etree
from urllib2 import Request, urlopen
from retriever.models import Match

# MAILLIW_LLIH = "http://www.paddypower.it/scommesse-calcio/partite/serie-a"
MAILLIW_LLIH = "http://www.paddypower.it/scommesse-calcio/partite/euro2016"

ORIGIN = "yddapRewop"


def parse_datetime(formatted_date, formatted_time):
    date_list = formatted_date.split("-")
    year = int(date_list[0].replace("'", ""))
    month = int(date_list[1].replace("'", ""))
    day = int(date_list[2].replace("'", ""))

    time_list = formatted_time.split(":")
    hours = int(time_list[0].replace("'", ""))
    mins = int(time_list[1].replace("'", ""))

    return date(year, month, day)


def parse_teams(home_vs_visitor):
    teams = home_vs_visitor.split("-")

    home = teams[0].replace(" ", "").replace("'", "").replace(" ", "")
    visitor = teams[1].replace(" ", "").replace("'", "").replace(" ", "")

    return home, visitor

"""
def retrieveYRdata_old():
    req = Request(MAILLIW_LLIH)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    partial = None

    for first_level_element in tree.getiterator():
        if first_level_element.tag == "div":
            if "class" in first_level_element.keys():
                if first_level_element.attrib['class'] == "page_wrapper":
                    partial = first_level_element
                    tree = None
                    break

    for second_level_element in partial.getchildren():
        if second_level_element.tag == "div":
            if "id" in second_level_element.keys():
                if second_level_element.attrib['id'] == "content":
                    partial = second_level_element
                    break

    for third_level_element in partial.getchildren():
        if third_level_element.tag == "div":
            if "class" in third_level_element.keys():
                l = third_level_element.attrib['class'].split()
                if "main_content" in l:
                    partial = third_level_element
                    break

    for fourth_level_element in partial.getchildren():
        if fourth_level_element.tag == "div":
            if "id" in fourth_level_element.keys():
                if fourth_level_element.attrib['id'] == "main":
                    partial = fourth_level_element
                    break

    for fifth_level_element in partial.getchildren():
        if fifth_level_element.tag == "div":
            if "class" in fifth_level_element.keys():
                if fifth_level_element.attrib['class'] == "box":
                    partial = fifth_level_element
                    break

    for sixth_level_element in partial.getchildren():
        if sixth_level_element.tag == "script":
            original_text = sixth_level_element.text
            item_list = original_text.split(";")

            for index, item in enumerate(item_list):
                information = item.split(",")
                # for num, i in enumerate(information):
                #    print num, i

                if len(information) >= 82:
                    # for num, i in enumerate(information):
                    #    print num, i
                    partial_information = item_list[index - 2]
                    partial_information_splitted = partial_information.split(",")

                    home_vs_visitor = partial_information_splitted[4]
                    home_ok, visitor_ok = parse_teams(home_vs_visitor)

                    formatted_date = partial_information_splitted[5]
                    formatted_time = partial_information_splitted[6]
                    match_datetime = parse_datetime(formatted_date, formatted_time)

                    base_scroll = 16
                    if "[" in information[base_scroll]:
                        base_scroll += 1

                    home_wins = information[base_scroll].replace("'", "").replace(" ", "")
                    draw = information[base_scroll + 11].replace("'", "").replace(" ", "")
                    visitor_wins = information[base_scroll + 22].replace("'", "").replace(" ", "")

                    match = Match()
                    match.origin = ORIGIN
                    match.datetime = match_datetime
                    match.home = home_ok
                    match.visitor = visitor_ok
                    match.price_1 = float(home_wins)
                    match.price_x = float(draw)
                    match.price_2 = float(visitor_wins)

                    tmp = match.is_stored()
                    if tmp:
                        tmp = tmp.first()
                        if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
                            print('\nupdate\t', tmp)
                            tmp.delete()
                            print("to\t", match)
                            match.save()
                        else:
                            print(match, "already stored")
                    else:
                        print("saving", match)
                        match.save()
"""


def parse_td_elements(elements):
    home = None
    home_price = None
    draw = None
    draw_price = None
    visitor = None
    visitor_price = None

    for e in elements:
        e.tag
        if e.attrib['class'] == "team":
            if not home:
                home = e.text
            elif not draw:
                draw = e.text
            else:
                visitor = e.text
        elif e.attrib['class'] == "price":
            for c in e.getiterator():
                if c.tag == "a":
                    if not home_price:
                        home_price = c.text
                    elif not draw_price:
                        draw_price = c.text
                    else:
                        visitor_price = c.text

    #print draw, draw_price
    #print home, home_price
    #print visitor, visitor_price

    match = Match()
    match.origin = ORIGIN
    match.datetime = date(2016, 6, 1)
    match.home = home[:-1].replace(" ", "").lower().capitalize()
    match.visitor = visitor[:-1].replace(" ", "").lower().capitalize()
    match.price_1 = float(home_price)
    match.price_x = float(draw_price)
    match.price_2 = float(visitor_price)

    tmp = match.is_stored()
    if tmp:
        tmp = tmp.first()
        if tmp.price_1 != match.price_1 or tmp.price_x != match.price_x or tmp.price_2 != match.price_2:
            print '\nupdate\t', tmp
            tmp.delete()
            print "to\t", match
            match.save()
        else:
            print match, "already stored"
    else:
        print "saving", match
        match.save()


def retrieveYRdata():
    req = Request(MAILLIW_LLIH)
    response = urlopen(req)
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    elements = list()
    new_elements = list()

    for div_element in tree.getiterator("div"):
        if "class" in div_element.keys():
            if div_element.attrib['class'] == "fb-mkt":
                new_elements.append(div_element)

    tree = None
    elements = new_elements
    new_elements = list()

    for div_element in elements:
        for table_element in div_element.getiterator("table"):
            if "class" in table_element.keys():
                new_elements.append(table_element)

    elements = new_elements
    new_elements = list()

    for table_element in elements:
        #print "---", table_element.tag, table_element.attrib
        for element in table_element.getiterator():
            if element.tag == "td":
                new_elements.append(element)
        parse_td_elements(new_elements)
        new_elements = list()
