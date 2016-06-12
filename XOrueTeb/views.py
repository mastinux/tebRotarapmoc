from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo :    html does not contain proper data
#           proceed in other way

ORUE_TEB = "http://web.eurobet.it/webeb/scommesse-sportive"

"""
req = Request(ORUE_TEB)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

myfile = open("my_html.txt", "w")
myfile.write(html.encode('utf-8'))
myfile.close()
"""

req = Request(ORUE_TEB)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

for element in tree.getiterator("div"):
    if "class" in element.keys() and element.attrib["class"] == "info_scommessa":
        print element.tag, element.attrib

# FIXME: can't access data