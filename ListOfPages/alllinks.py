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

from featuresForMeetingPageOrNot import GetNumberOfTimes,GetNumberOfAddresses,GetPresenceOfDays,GetPresenceOfWordMeeting,GetPresenceOfWordMeetingInURL

########################################################################################################################################
##Given URL string, output the type of the page##
########################################################################################################################################
def FindPageType(pageURL):
	if ".HTM".lower() in pageURL.lower():
		return "HTML"
	elif ".asp".lower() in pageURL.lower():
		return "ASP"
	elif ".php".lower() in pageURL.lower():
		return "PHP"
	elif "https://docs.google.com/document/".lower() in pageURL.lower():
		return "Google DOC"
	elif "https://docs.google.com/spreadsheets/".lower() in pageURL.lower():
		return "Google SPREADSHEET"
	
	elif pageURL.lower().endswith(".pdf".lower()):
		return "PDF"
	elif pageURL.lower().endswith(".doc".lower()):
		return "DOC"
	elif pageURL.lower().endswith(".docx".lower()):
		return "DOCX"
	elif pageURL.lower().endswith(".jpg".lower()) or pageURL.lower().endswith(".png".lower()) or pageURL.lower().endswith(".bmp".lower()):
		return "IMAGE"
	elif ".org".lower() in pageURL.lower() or ".com".lower() in pageURL.lower():
		return "WEBPAGE"
	else:
		return "UNKNOWN"

########################################################################################################################################
##Cancel if there is an alert##
########################################################################################################################################

def AlertDismiss(dvr):
	print "call alert"
	try:
	    '''WebDriverWait(dvr, 0.5).until(EC.alert_is_present(),
		                           'Timed out waiting for PA creation ' +
		                           'confirmation popup to appear.')'''

	    alert = dvr.switch_to_alert()
	    alert.dismiss()
	    print "alert"
	except Exception as e:
	    print "no-alert"
	    pass


#starting external display
display = Display(visible=0, size=(1024, 768))
display.start()

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


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 3)

for one_state in state_array:
    dirname_state="../"+one_state.name
    if not os.path.exists(dirname_state):
    	os.makedirs(dirname_state)

    for city in one_state.cities:
	#print city.cityname
	

	if city.cityaaurl and "Not available" not in city.cityaaurl:
		homeurl=city.cityaaurl
		if not homeurl.startswith("http"):
			homeurl="http://"+homeurl

		listofurl=Queue()
		
		count=5
		urls=[]
		try:
			browser.get(homeurl)
			#AlertDismiss(browser)
			browser.switch_to_alert().dismiss()
		except:
			pass
		homeurl=browser.current_url
		urls.append(homeurl)
		#making the list for writing to CSV
###################################################################
#####################################################################
		
		listofurl.enqueue(homeurl)
		listofurl.enqueue("$$")
		while listofurl.size()>0:

			#print
			if count==0:
				break
			anurl=listofurl.dequeue()
			
			if anurl=="$$":
				count=count-1
				continue
			else:	
				if not anurl.startswith("http"):
					anurl="http://"+anurl
			
					try:
						browser.get(anurl)
						browser.switch_to_alert().dismiss()
				   	except : 
						pass
					#AlertDismiss(browser)
					print "calling asp after"
					#pagetext=browser.page_source
					#print pagetext
					##########################################################################################

					##########################################################################################
					try:
						links=browser.find_elements_by_tag_name("a")
						for link in links:
							page=link.get_attribute("href")
							#print page



							if not page.startswith("http"):
								page="http://"+page
						
							withoutwwwlist=page.split("www.")
							if len(withoutwwwlist)>1:
								wwwminus=withoutwwwlist[1]
							else:
								wwwminus=page

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
								#print page
					
						for link in urls:
							#print "link is"+link
							#print link.current_url
							if not link.startswith("http"):
									link="http://"+link 
							try:
								browser.get(link)
								AlertDismiss(browser)
								submit_BUTTON_XPATH = '//input[@type="submit"]'
								button = browser.find_element_by_xpath(submit_BUTTON_XPATH)
								if button is not None:	
									button.click()
									#txt=browser.page_source
									#print txt
									#fo = open("meetingtext.html", "wb")
									#fo.write(txt)
									print "form found"
								page=browser.current_url

								##########################################################################################
								
##########################################################################################

					except Exception as err2:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
						#print(exc_type, fname, exc_tb.tb_lineno)
						#print str(err2)	
						pass


					listofurl.enqueue("$$")


		#print (len(urls))
		print city.cityname
		#print urls
		'''with open("../"+one_state.name+"/"+city.cityname+".csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(list_row)'''


#browser.quit() # Quit the driver and close every associated window.
#display.stop()


def FindPageType(pageURL):
	if ".HTML".lower() in pageURL.lower():
		return "HTML"
	elif ".asp".lower() in pageURL.lower():
		return "ASP"
	elif ".php".lower() in pageURL.lower():
		return "PHP"
	elif "https://docs.google.com/document/".lower() in pageURL.lower():
		return "Google DOC"
	elif "https://docs.google.com/spreadsheets/".lower() in pageURL.lower():
		return "Google SPREADSHEET"
	
	elif pageURLlower().endswith(".pdf".lower()):
		return "PDF"
	elif pageURLlower().endswith(".doc".lower()):
		return "DOC"
	elif pageURLlower().endswith(".jpg".lower()) or pageURLlower().endswith(".png".lower()) or pageURLlower().endswith(".bmp".lower()):
		return "IMAGE"
	else:
		return "UNKNOWN"
	





