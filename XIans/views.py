from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
import execjs
from webbrowser import open as webbrowser_open
import selenium.webdriver as webdriver

IANS = "https://www.snai.it/sport"
ORIGIN = "Ians"


def parse_datetime(formatted_date, formatted_time):
    print formatted_date, formatted_time


def parse_teams(home_vs_visitor):
    print home_vs_visitor


def retrieveHtml():
    req = Request(IANS)
    response = urlopen(req)
    html = response.read()

    return html


url = ""

driver = webdriver.Firefox()
driver.get(url)
html = driver.page_source.encode('utf-8')
driver.quit()

f = open("page.html", "w")
f.write(html)
f.close()
