from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time ,os ,re,sys, csv
from xml.etree import ElementTree
from stateinfo import CityURL
from stateinfo import URLbyState
from queueClass import Queue

from HelperFunctions import FindPageType,SetHeaderOfCSV,SetARowOfCSV,IsValidWebpage
from featuresForMeetingPageOrNot import GetNumberOfTimes,GetNumberOfAddresses,GetPresenceOfDays,GetPresenceOfWordMeeting,GetPresenceOfWordMeetingInURL

forbidden=["http://www.dutchessaa.org/Member_Area.html"]



def SetCSVForACity(homeurl,rowoflist):
	count=5
	listofurl=Queue()
	urls=[]
	url=homeurl
	listofurl.enqueue(url)
	urls.append(url)
	listofurl.enqueue("$$")
	list_row=rowoflist
	while listofurl.size()>0:
		if count==0:
			break
		anurl=listofurl.dequeue()
			
		if anurl=="$$":
			count=count-1
			continue
		else:
			links=[]
			flagd=0
			try:
				if anurl in forbidden:
					continue
				browser.get(anurl)
				
				textofpage=browser.page_source	
				SetARowOfCSV(list_row,anurl,textofpage,FindPageType(anurl))

			except Exception as notopen:
				print str(notopen)
				pass
				
			try:
				browser.switch_to_alert().accept()
			except:
				pass
			try:
				browser.switch_to_alert().dismiss()
			except:
				pass
				
			try:	
				#links=browser.find_elements_by_tag_name("a")
				LINK_XPATH = '//*[@href or @src]'
				links = browser.find_elements_by_xpath(LINK_XPATH)
			except Exception as ex:
				#print ex
				pass
			for link in links:																#######href in a######################
				try:
					page=""
					if link.get_attribute("href"):
						page=link.get_attribute("href")
					elif link.get_attribute("src"):
						page=link.get_attribute("src")
					#print page
					pagetype=FindPageType(page)
					if IsValidWebpage(page,url,urls):
						listofurl.enqueue(page)
						urls.append(page)
						flagd=1
				except:
					pass
			
			
			submit_BUTTON_XPATH = '//*[@type="submit"]'
			buttons = browser.find_elements_by_xpath(submit_BUTTON_XPATH)				
			for bnum in range(len(buttons)):
				page=""
				try:
					if buttons[bnum].is_displayed():
					
						buttons[bnum].click()
						page=browser.current_url
				except:
						pass		
				try:
					browser.switch_to_alert().accept()
				except:
					pass
				if page:
					try:
						pagetype=FindPageType(page)
						if IsValidWebpage(page,url,urls):
							#listofurl.enqueue(page)
							urls.append(page)
							textofpage=browser.page_source
							SetARowOfCSV(list_row,page,textofpage,pagetype)
					except:
						pass						
					
				try:
					browser.get(anurl)
				except:
					pass
				try:
					browser.switch_to_alert().dismiss()
				except:
					pass
				
			submit_BUTTON_XPATH = '//*[@type="button"]'
			buttons = browser.find_elements_by_xpath(submit_BUTTON_XPATH)				
			for bnum in range(len(buttons)):
				page=""
				if buttons[bnum].is_displayed():
					try:
						buttons[bnum].click()
						page=browser.current_url
					except:
						pass		
				try:
					browser.switch_to_alert().accept()
				except:
					pass
				if page:
					try:
						pagetype=FindPageType(page)
						if IsValidWebpage(page,url,urls):
							#listofurl.enqueue(page)
							urls.append(page)
							textofpage=browser.page_source
							SetARowOfCSV(list_row,page,textofpage,pagetype)
					except:
						pass						
					
				try:
					browser.get(anurl)
				except:
					pass
				try:
					browser.switch_to_alert().dismiss()
				except:
					pass
				
			
			listofurl.enqueue("$$")
			#listofurl.printqueue()
			
	if listofurl.size()>0:	
		anurl=listofurl.dequeue()
			
		if anurl is not "$$":
			try:
				browser.get(anurl)			
				textofpage=browser.page_source	
				SetARowOfCSV(list_row,anurl,textofpage,FindPageType(anurl))
			except Exception as notopen:
				print str(notopen)
				pass
				
			try:
				browser.switch_to_alert().accept()
			except:
				pass
			try:
				browser.switch_to_alert().dismiss()
			except:
				pass
			
	'''myfile = open("tricity.csv", 'wb')
	writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for word in urls:
		writer.writerow([word])'''

	with open("../States/"+one_state.name+"/"+city.cityname+".csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(list_row)
		
	#print urls
	#print listofurl.printqueue()
		
				
				
				
#starting external display
#display = Display(visible=0, size=(1024, 768))
#display.start()

#declaring objects needed to save data after parsing
state_array=[]

#parsing xml for setting the states, cities and URLs of the AA homepages
document = ElementTree.parse( 'abcd.xml' )
states= document.getroot()
for one_state in states.findall( 'state' ):
    state_name=one_state.find('state_name').text
    city_array=[]
    for cities in one_state.findall( 'cities/city'):
	city_name=cities.find('city_name').text
	city_url=cities.find('city_url').text
	one_city=CityURL(city_name,city_url)
	city_array.append(one_city)

    state=URLbyState(state_name,city_array)
    state_array.append(state)
#done xml parsing, now go through the array and apply BFS to extract all the pages till 4th level (count-1)
#create folder with state name, for each city, one csv file

browser = webdriver.Chrome("C:\Users\Bittamoni\Downloads\chromedriver.exe")
wait = WebDriverWait(browser, 3)

for one_state in state_array:
    dirname_state="../States/"+one_state.name
    if not os.path.exists(dirname_state):
    	os.makedirs(dirname_state)

    for city in one_state.cities:
		print city.cityname
		listrow=[]
		SetHeaderOfCSV(listrow)

		if city.cityaaurl and "Not available" not in city.cityaaurl:
			homeurl=city.cityaaurl
			if homeurl and not homeurl.startswith("http"):
				homeurl="http://"+homeurl
			
			SetCSVForACity(homeurl,listrow)
				
				
				

