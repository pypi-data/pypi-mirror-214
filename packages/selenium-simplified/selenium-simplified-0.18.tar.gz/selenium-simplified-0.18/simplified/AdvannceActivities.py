from selenium.webdriver.common.by import By
import time
from datetime import datetime


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("background: blue; border: 2px solid orange;")
    time.sleep(.3)
    apply_style(original_style)
    return True


class AdvanceActivities:
    def __init__(self, driver):
        self.driver = driver

    def click_screenshot(self, dir):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        current_date = dt_string.split(" ")[0].replace('/','_')
        current_time = dt_string.split(" ")[1].replace(':', '_')
        file_name = current_date+'_'+current_time.replace(':','_')+".png"
        self.driver.save_screenshot(dir+file_name)

