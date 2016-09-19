from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time ,os ,re
from Converters import PDFtoTextConvert 
from Converters import document_to_text



def GetNumberOfTimes(text):
	arr=["1 pm","2 pm","3 pm","4 pm","5 pm","6 pm","7 pm","8 pm","9 pm","10 pm","11 pm","12 pm","1 am","2 am","3 am","4 am","5 am","6 am","7 am","8 am","9 am","10 am","11 am","12 am","1pm","2pm","3pm","4pm","5pm","6pm","7pm","8pm","9pm","10pm","11pm","12pm","1am","2am","3am","4am","5am","6am","7am","8am","9am","10am","11am","12am"]
	text=text.replace("&nbsp;"," ")
	text=text.replace("<"," ")
	text=text.lower()
	line=text
	count=0
	for el in arr:
		if el in line:
			count=count+line.count(el)
	grp=re.finditer('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)', line,re.I|re.M)
	
	re.sub('\d{1,2}(:(\d{2})*)\s*(AM|am|PM|pm|a|p)','',line)
	#print line
	#grp2=re.finditer('\d{1,2}\s{0,1}(AM|am|PM|pm)', line,re.I|re.M)

	'''for p in grp:
	    print p.start()'''
	return sum(1 for e in grp) +count

def GetNumberOfAddresses(text):

	line=text
	#grp=re.finditer(r'\d{1,2}(?:(?:am|pm)|(?::\d{1,2})( )(?:am|pm)?)', line,re.I|re.M)
	street_address = re.finditer('\d{1,4} [\w\s\,\.]{0,20}(?:street|st|avenue|av|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)',line,re.I|re.M)
	
	'''for p in street_address:
	    print p.group()'''
	addsum=sum(1 for e in street_address)
	chcount=text.lower().count("Church".lower())
	allsum=addsum+chcount
	return allsum

def GetPresenceOfDays(text):
	text=text.lower()
	return int(("Sunday".lower() in text or "Sun".lower() in text) and ("Monday".lower() in text or "Mon".lower() in text) and ("Tuesday".lower() in text or "Tue".lower() in text or "Tues".lower() in text) and ("Wednesday".lower() in text or "Wed".lower() in text) and ("Thursday".lower() in text or "Thurs".lower() in text) and ("Friday".lower() in text or "Fri".lower() in text) and ("Saturday".lower() in text or "Sat".lower() in text))

def GetPresenceOfWordMeeting(text):
	return text.lower().count("Meeting".lower())

def GetPresenceOfWordMeetingInURL(url):
	return int("meeting".lower() in url.lower())

'''browser = webdriver.Chrome("C:\Users\Bittamoni\Downloads\chromedriver.exe")
browser.get("http://www.fairbanksaa.org/intergroup/fbksintergroup.html")
print GetNumberOfTimes(browser.page_source)
print GetNumberOfAddresses(browser.page_source)'''
#print GetPresenceOfDays(document_to_text('example files/District 05 Meeting List.doc'))
#print GetPresenceOfWordMeeting(document_to_text('example files/District 05 Meeting List.doc'))
#print GetPresenceOfWordMeetingInURL(browser.current_url)







	
