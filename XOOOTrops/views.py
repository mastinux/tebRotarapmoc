from lxml import etree
from io import StringIO
import selenium.webdriver as webdriver
from pyvirtualdisplay import Display
#from retriever.models import Match


def retrieveOTdata(url):
    print "processing oootroops"

    display = Display(visible=0, size=(1024, 1024))
    display.start()

    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    driver.quit()

    display.stop()

    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
