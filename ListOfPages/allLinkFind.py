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

from HelperFunctions import FindPageType,SetHeaderOfCSV,SetARowOfCSV













#starting external display
#display = Display(visible=0, size=(1024, 768))
#display.start()

#declaring objects needed to save data after parsing
state_array=[]

#parsing xml for setting the states, cities and URLs of the AA homepages
document = ElementTree.parse( 'AllAAHomePages.xml' )
states= document.getroot()
for one_state in states.findall( 'state' ):
    state_name=one_state.find('state_name').text
    city_array=[]
    for cities in one_state.findall( 'cities/city' ):
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
    dirname_state="../"+one_state.name
    if not os.path.exists(dirname_state):
    	os.makedirs(dirname_state)

    for city in one_state.cities:
	print city.cityname

	rowcount=0
	list_row=[]
	SetHeaderOfCSV(list_row)

	if city.cityaaurl and "Not available" not in city.cityaaurl:
		homeurl=city.cityaaurl
		if homeurl and not homeurl.startswith("http"):
			homeurl="http://"+homeurl

		listofurl=Queue()
		urls=[]
		count=5
		try:
			browser.get(homeurl)
			#AlertDismiss(browser)
			browser.switch_to_alert().dismiss()
		except:
			#print "no alert"
			pass

		homeurl=browser.current_url
		urls.append(homeurl)
		listofurl.enqueue(homeurl)
		listofurl.enqueue("$$")

		while listofurl.size()>0:
			if count==0:
				break
			anurl=listofurl.dequeue()
			
			if anurl=="$$":
				count=count-1
				continue
			else:	
				if anurl and not anurl.startswith("http"):
					anurl="http://"+anurl
				ftype=FindPageType(anurl)

				print ftype
				if ftype is "HTML" or ftype is "PHP" or ftype is "ASP" or ftype is "WEBPAGE":
					print "appending2:"+anurl
					textofpage=browser.page_source	
					SetARowOfCSV(list_row,anurl,textofpage,ftype)
					'''list_row.append([])		
					rowcount=rowcount+1
					list_row[rowcount].append(anurl)
					list_row[rowcount].append(ftype)
					list_row[rowcount].append(GetNumberOfTimes(textofpage))
					list_row[rowcount].append(GetNumberOfAddresses(textofpage))
					list_row[rowcount].append(GetPresenceOfDays(textofpage))
					list_row[rowcount].append(GetPresenceOfWordMeetingInURL(browser.current_url))
					list_row[rowcount].append(GetPresenceOfWordMeeting(textofpage))'''
			
				try:
					browser.get(anurl)
					browser.switch_to_alert().dismiss()
				except : 
					pass
				
				links=browser.find_elements_by_tag_name("a")
				for link in links:
					try:
						page=link.get_attribute("href")
						#print page
					

						if page and  not page.startswith("http"):
							page="http://"+page
				
						withoutwwwlist=page.split("www.")
						if len(withoutwwwlist)>1:
							wwwminus=withoutwwwlist[1]
						else:
							wwwminus=page
					except:
						pass

					withoutwwwlist=homeurl.split("www.")
					if len(withoutwwwlist)>1:
						homewwwminus=withoutwwwlist[1]
					else:
						homewwwminus=homeurl
					#print "page:"+wwwminus
					#print "home:"+homewwwminus
					if page and homewwwminus in wwwminus and page not in urls and "www.aa.org" not in page and not page.endswith(".js") and not page.endswith(".css"):
						listofurl.enqueue(page)
						urls.append(page)

				for link in urls:
					if link and not link.startswith("http"):
							link="http://"+link 
					try:
						browser.get(link)
						browser.switch_to_alert().dismiss()
						
						submit_BUTTON_XPATH = '//input[@type="submit"]'
						button = browser.find_element_by_xpath(submit_BUTTON_XPATH)
						if button is not None:	
							button.click()
							#txt=browser.page_source
							#print txt
							#fo = open("meetingtext.html", "wb")
							#fo.write(txt)
							#print "form found"
						page=browser.current_url
					except:
						pass

				listofurl.enqueue("$$")

				

		with open("../"+one_state.name+"/"+city.cityname+".csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(list_row)




































