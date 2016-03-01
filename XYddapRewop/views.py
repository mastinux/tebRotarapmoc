from django.shortcuts import render

from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import datetime
from retriever.models import Match

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

MAILLIW_LLIH = "http://www.paddypower.it/scommesse-calcio/partite/serie-a"
ORIGIN = "yddapRewop"


def parse_datetime(formatted_date, formatted_time):
    date_list = formatted_date.split("-")
    year = int(date_list[0].replace("'", ""))
    month = int(date_list[1].replace("'", ""))
    day = int(date_list[2].replace("'", ""))

    time_list = formatted_time.split(":")
    hours = int(time_list[0].replace("'", ""))
    mins = int(time_list[1].replace("'", ""))

    return datetime(year, month, day, hours, mins)


def parse_teams(home_vs_visitor):
    teams = home_vs_visitor.split("-")

    home = teams[0].replace(" ", "").replace("'", "")
    visitor = teams[1].replace(" ", "").replace("'", "")

    return home, visitor


def retrieveYRdata():
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
    """
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    indented_html = etree.tostring(tree, pretty_print=True)
    my_file = open("tmp_file.txt", "w")
    my_file.write(indented_html.encode('utf-8'))
    my_file.close()
    """

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
                #for num, i in enumerate(information):
                #    print num, i

                if len(information) >= 82:
                    #for num, i in enumerate(information):
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
                            print "\nupdate\t", match
                            tmp.price_1 = match.price_1
                            tmp.price_x = match.price_x
                            tmp.price_2 = match.price_2
                            match = tmp
                            match.update()
                            #tmp.update()
                            print "to\t", tmp
                        else:
                            print tmp, "already stored"
                    else:
                        print "saving", match
                        match.save()