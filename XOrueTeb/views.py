from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO

# todo :    html does not contain proper data
#           proceed in other way

ORUE_TEB = "http://web.eurobet.it/webeb/scommesse-sportive"


req = Request(ORUE_TEB)
response = urlopen(req)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

myfile = open("my_html.txt", "w")
myfile.write(html.encode('utf-8'))
myfile.close()