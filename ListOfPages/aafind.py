from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
browser = webdriver.Chrome()
browser.get("http://www.aa.org/pages/en_US/find-aa-resources?zipcode=Zip%2FPostal+Code") 
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'column'))) 
states = browser.find_elements_by_class_name("column")	

for state in states:
	print 	state.text			
	state.click()
	browser.implicitly_wait(5)
	links=browser.find_elements_by_tag_name("a")
	for link in links:
		print link.get_attribute("href")
	break
	#browser.execute_script("window.history.go(-1)")



