from django.shortcuts import render
from HTMLParser import HTMLParser
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# fixme : html does not report proper data

ORUE_TEB = "http://web.eurobet.it/webeb/scommesse-sportive"


req = Request(ORUE_TEB)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

myfile = open("my_html.txt", "w")
myfile.write(html.encode('utf-8'))
myfile.close()

#parser = etree.HTMLParser()
#tree = etree.parse(StringIO(html), parser)