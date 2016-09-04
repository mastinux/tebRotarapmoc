from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
#from retriever.models import Match

ORIGIN = "TenTeb"


def retrieveTTdata(url):
    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)

    for div_element in tree.getiterator("div"):
        if "id" in div_element.keys():# and div_element.attrib["id"] == "updatableWindowsContainer":
            print div_element.keys()


retrieveTTdata("")
