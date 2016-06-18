from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

ORUE_TEB = ""

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
    if "class" in element.keys() and element.attrib["class"] == "":
        print element.tag, element.attrib