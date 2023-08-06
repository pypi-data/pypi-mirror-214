from ..CommonActivities import *
from .IdentifyLocators import ParseDOM


class LocatorSpider:
    def __init__(self, driver):
        self.dom_crawler = ParseDOM
        self.driver = driver

    def crawler_input(self):
        locator = self.dom_crawler.crawler_input(self, source=self.driver.get_html_source())
        [highlight(element=self.driver.web_element(xpath=path)) for xpath in locator for path in xpath]







