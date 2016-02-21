from django.db import models
from HTMLParser import HTMLParser
from urllib2 import urlopen, Request
import sys
# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

ORUE_TEB = "'http://web.eurobet.it/webeb/scommesse-sportive'"


class OrueTebParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag: <", tag, ">"

    def handle_endtag(self, tag):
        print "Encountered an end tag : </", tag, ">"

    def handle_data(self, data):
        print "Encountered some data  :", data


req = Request(ORUE_TEB)
response = urlopen(req)
html = response.read()
print html
#html_encoded = html.decode('utf-8')

#parser = OrueTebParser()
#parser.feed(html)