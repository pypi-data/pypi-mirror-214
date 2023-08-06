from ..CommonActivities import *
from .IdentifyLocators import ParseDOM


class LocatorSpider:
    def __init__(self, driver):
        self.dom_crawler = ParseDOM
        self.driver = driver

    def give_locator_of_all_input_Boxes(self):
        return self.dom_crawler.give_locator_all_inputBoxes(self, source=self.driver.get_html_source())

    def give_locator_of_all_input_Boxes_and_highlight(self):
        locator = self.dom_crawler.give_locator_all_inputBoxes(self, source=self.driver.get_html_source())
        [highlight(element=self.driver.web_element(xpath=path)) for xpath in locator for path in xpath]
        return locator







