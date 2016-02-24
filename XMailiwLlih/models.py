from django.db import models
from HTMLParser import HTMLParser
from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo : continue surfing the DOM

# https://docs.python.org/2/library/htmlparser.html
# https://docs.python.org/2/howto/urllib2.html

# http://lxml.de/tutorial.html

# http://lxml.de/api/lxml.etree._ElementTree-class.html
# http://lxml.de/api/lxml.etree._Element-class.html

MAILLIW_LLIH = "http://sports.williamhill.it/bet_ita/it/betting/t/321/Serie+A.html"


class EchoTarget(object):

    def start(self, tag, attrib):
        # single interesting row
        if tag == "tr":
            print type(self)
            print "\ntag :", tag
            for k, v in attrib.items():
                print "\tattr :", k, "=", v

    #def data(self, data):
    #    print("\n[data] %r" % data)

    """
    def end(self, tag):
        print("end %s" % tag)

    def comment(self, text):
        print("comment %s" % text)
    """
    def close(self):
        print("\n[close]")
        return "closed!"


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
    #print o
    #print type(o)
    if o.tag == "tr":
        # 	o.find(self, path, namespaces=None)     # Finds the first matching subelement, by tag name or path.
        #   o.findall(self, path, namespaces=None)  # Finds all matching subelements, by tag name or path.
        #   o.get(self, key, default=None)          # Gets an element attribute.
        #   o.getchildren(self)                     # Returns all direct children. The elements are returned
        # in document order.
        #   o.getiterator(self, tag=None, *tags)    # Returns a sequence or iterator of all elements in the subtree
        # in document order (depth first pre-order), starting with this element.
        #   o.items(self)                           # Gets element attributes, as a sequence. The attributes
        # are returned in an arbitrary order.
        #   o.keys(self)                            # Gets a list of attribute names. The names are returned
        # in an arbitrary order (just like for an ordinary Python dictionary).
        #   o.values(self)                          # Gets element attribute values as a sequence of strings.
        # The attributes are returned in an arbitrary order.
        print "\n", o.tag, "\n", o.attrib
        for c in o.getchildren():
            print c.tag
