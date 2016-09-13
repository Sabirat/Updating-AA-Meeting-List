

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].style.background='yellow'",
                              element)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 5px solid red;")
    apply_style("border: 5px solid red;")
    time.sleep(.3)
    #apply_style(original_style)


browser = webdriver.Chrome()
#browser.get("http://www.birminghamaa.org/meetings.php")
browser.get("http://www.edmontonaa.org/find-a-meeting")
for e in browser.find_elements_by_xpath('//tr'):
	print e.location
	print e.size
	highlight(e)

print "another"
