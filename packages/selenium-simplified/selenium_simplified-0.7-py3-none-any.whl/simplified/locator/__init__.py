from ..UserActivities import *
from .TagsLocator import *


class DOMInspector:
    def __init__(self, url):
        self.activities = CommonActivities()
        self.dom = ParseDOM()
        self.url = url

    def input_spider(self):
        locator = self.dom.xpath_input_tag(self.url)
        for xpath in locator:
            web_element = self.activities.find_element(xpath=xpath)
            highlight(element=web_element)





