from ..UserActivities import *
from .TagsLocator import ParseDOM as dom_crawler


class DOMCrawler:
    def __init__(self):
        self.dom_crawler = dom_crawler

    def crawler_input(self, driver):
        locator = self.dom_crawler.crawler_input(self, source=driver.get_html_source())
        [highlight(element=driver.web_element(xpath=path)) for xpath in locator for path in xpath ]







