from django.db import models
from HTMLParser import HTMLParser
from urllib2 import urlopen, Request
import sys
# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

ORUE_TEB = "http://web.eurobet.it/webeb/scommesse-sportive"

# todo : html does't contain proper values, check next site


class OrueTebParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            #print "\n"
            for name, value in attrs:
                print value
                if name == 'class' and value == 'box_container_scommesse_quote':
                    print value

    #def handle_endtag(self, tag):
    #    print "Encountered an end tag : </", tag, ">"

    #def handle_data(self, data):
    #    print "data :\t\t", data


req = Request(ORUE_TEB)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

parser = OrueTebParser()
parser.feed(html)
