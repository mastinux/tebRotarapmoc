from urllib2 import urlopen, Request
from lxml import etree
from io import StringIO
from datetime import date
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
#from retriever.models import Match

ORIGIN = "Agniw"


def retrieveAdata(url):
    display = Display(visible=0, size=(1024, 1024))
    display.start()
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    html = html.encode('utf-8')
    driver.quit()
    display.stop()

    print html
