from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time ,os ,re

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement


def findURL(input_string):
    # print input_string
    if "Site:" in input_string:
	line = input_string[input_string.find('www'):]
	#print line
	end=line.find('"')
	line = line[0:end]
	print line
	if "%" in line:
		line = line[0:line.find('%')+1]
		line.split()
		if "\n" not in line:
			line = line + '\n'
	#print line		
	return line


output_file = open( 'AllAAHomePages.xml', 'w' )
output_file.write( '<?xml version="1.0"?>' )
statesXML = Element( 'states' )

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 3)
browser.get("http://www.aa.org/pages/en_US/find-aa-resources?zipcode=Zip%2FPostal+Code")
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'column'))) 
states = browser.find_elements_by_class_name("column")	
state_set = set()
state_lst = []
state_names=[]
for state in states:
	state_lst.append(state.get_attribute('id').encode('ascii','replace'))
	state_names.append(state.text)

ind=0
for cur_state in state_lst:
	stname=state_names[ind]
	stateInfo = SubElement( statesXML, 'state' )
	StateInfoChildName=SubElement( stateInfo, 'state_name')
	StateInfoChildName.text=stname
	StateInfoCities=SubElement( stateInfo, 'cities')
	ind=ind+1
	#print type(cur_state)
	str = "document.getElementById('" + cur_state + "').click()"
	#smaller_header = browser.find_elements_by_class_name("smaller_header")
	
	wait.until(EC.visibility_of_element_located((By.ID, cur_state)))
	time.sleep(2)
	try:
		browser.execute_script(str)
	#browser.execute_script(str)
	#if smaller_header != browser.find_elements_by_class_name("smaller_header"):
		wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'item-cell')))
		items= browser.find_elements_by_class_name("item-cell")
		for item in items:
			city=item.find_element_by_class_name("city")
			#print city.text
			#print findURL(item.text)
			cityChild=SubElement( StateInfoCities, 'city')
			cityname = SubElement( cityChild, 'city_name' )
			cityname.text=city.text
			cityurlxml = SubElement( cityChild, 'city_url' )
			onepara=item.find_element_by_class_name("item")
			c_url=findURL(item.get_attribute('innerHTML'))
			if c_url is not None:
				cityurlxml.text=c_url
			else:
				cityurlxml.text="Not available"
		#fd.write(browser.page_source.encode("utf8"))
		scriptText=browser.page_source.encode("utf8")
		#print scriptText
	except TimeoutException:
		scriptText=browser.page_source.encode("utf8")
		#print scriptText
	except:
		print "exception"
	
	browser.get("http://www.aa.org/pages/en_US/find-aa-resources?zipcode=Zip%2FPostal+Code")
	wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'column')))



output_file.write( ElementTree.tostring( statesXML ) )
output_file.close()


