from ..UserActivities import *
from .TagsLocator import *


class DOMInspector:
    def __init__(self, url, driver):
        self.activities = CommonActivities(driver=driver)
        self.spider = ParseDOM()
        self.url = url

    def input_spider(self):
        locator = self.spider.spider_input(url=self.url)
        for xpath in locator:
            web_element = self.activities.find_element(xpath=xpath)
            highlight(element=web_element)





