import collections
import codecs
import time
from classes import PatternString, TreeNode, Sequence, MLStripper, URLInfo, FormInfo,MeetingInfo,Position
from Features import GetNumberOfTimes, GetNumberOfAddresses, GetPresenceOfDays, GetMissingAddress, GetMissingDay
from PageFilter import readPageInString, traverse, traversePrint, SetSubtrees, FindDuplicates, FindTags
from MeetingInformationExtractionFunctions import GetMeetingTime, GetMeetingAddress,GetMeetingDay,RemoveHTMLTags
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from xlrd import open_workbook
import string
from Database import InitDatabase,InsertMeeting


from BeautifulSoup import BeautifulSoup

browser = webdriver.Chrome()#("C:\Users\Bittamoni\Downloads\chromedriver.exe")
#browser.set_window_size(1180,800)
txt=""
mptc=40	#maxiumum # of patterns to consider
wAddress=0.3
wTime=0.4


#connection=InitDatabase()


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    print "highlighting element"
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].style.background='yellow'",
                              element)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 5px solid red;")
    apply_style("border: 5px solid red;")
    #time.sleep(.3)
    #apply_style(original_style)

def HighlightMeeting(pattern,initialPage):
	
	first_tag=pattern.patString.split(',')[0]
	print "highlight called:"+pattern.patString

	pagesubstring= initialPage[pattern.start:pattern.end]
	soup=BeautifulSoup(pagesubstring)
	souptext=soup.text
	filtered_soup = filter(lambda x: x in string.printable, souptext)
	
	for e in browser.find_elements_by_xpath("//"+first_tag):#browser.find_elements_by_xpath(".//"+first_tag+"[contains(text(), \""+soup.text+"\")]"):
		content=browser.execute_script("return arguments[0].textContent", e)
		filtered_elemtext=filter(lambda x: x in string.printable, content)
		filtered_elemtext="".join(filtered_elemtext.split())
		#print e.location
		#print e.size
		#ihtml=e.get_attribute('outerHTML')
		#print "ou html:"+ihtml
		#print "page:"+initialPage[pattern.start:pattern.end]
		
		'''if "Sunday Morning Open Group" in e.text and "Sunday Morning Open Group" in initialPage[pattern.start:pattern.end]:
			print "html:"+e.text.strip()#ihtml.lower()
			print "inipage:"+soup.text.replace(" ","")
			l1=browser.page_source[pattern.start:pattern.end].lower()
			l2=ihtml.lower()
			print "html:"+ihtml.lower()
			print "inipage:"+initialPage[pattern.start:pattern.end].lower()
			for v in range(0,len(l2)):
				if l1[v]!=l2[v]:
					print "mismatch:"+str(ord(l1[v]))+"l2"+str(ord(l2[v]))+"ss"+str(v)
					print l1[210:240]
					print l2[210:240]
					break
		pagesubstring= initialPage[pattern.start:pattern.end]
		soup=BeautifulSoup(pagesubstring)'''
		etext=e.text
		#filtered_elemtext=filter(lambda x: x in string.printable, etext)
		if pattern.patString=="tr,$$td,td,td,td,td,td,td,td,$$font,font,font,font,font,font,font,font,$$a,$$":
			print "elem:"+filtered_elemtext#ihtml.lower()
			print "pattern:"+filtered_soup
		if filtered_elemtext.replace(" ","") ==filtered_soup.replace(" ",""):
			#print ihtml.lower()
			#print "inipage:"+pagesubstring.lower()
			browser.execute_script("return arguments[0].scrollIntoView();", e)
			highlight(e)

def FindMeetingXY(pattern,iniPage,day,time,address):
	
	first_tag=pattern.patString.split(',')[0]
	
	pagesubstring= iniPage#[pattern.start:pattern.end]
	#print "text:"+iniPage
	soup=BeautifulSoup(pagesubstring)
	souptext=soup.text
	filtered_soup = filter(lambda x: x in string.printable, souptext)
	
	earr=browser.find_elements_by_xpath("//"+first_tag)
	for e in earr[:]:#browser.find_elements_by_xpath(".//"+first_tag+"[contains(text(), \""+soup.text+"\")]"):
		content=browser.execute_script("return arguments[0].textContent", e)
		filtered_elemtext=filter(lambda x: x in string.printable, content)
		filtered_elemtext="".join(filtered_elemtext.split())

		etext=e.text
		if filtered_elemtext.replace(" ","") ==filtered_soup.replace(" ",""):
			mPos=Position(e.location['x'],e.location['y'],e.size['width'],e.size['height'])
			mUrl=browser.current_url
			mCity="Rochester, Minnesota"
			mFtag=first_tag
			mFulltext=pagesubstring
			earr.remove(e)
			OneMeeting=MeetingInfo(day,time,address,mUrl,mCity,mFulltext,mFtag,mPos,e.id)
			#print OneMeeting.__dict__
			#InsertMeeting(connection,OneMeeting)
			#e.screenshot("/Screenshots/foo.png")
# this function tries to find missing day or address in parent node starting from immediate parent and continuing till 10 level of ancestors
def FindInfoInParents(cNode,tillindex,missingDay,missingAddress):
	parent=cNode.parent
	found=0
	cnt=0
	while not found:
		if cnt==10:
			break
		cnt+=1
		if GetNumberOfAddresses(initialPage[parent.position:tillindex])==1:
			print "one address"
			print cNode.tagname
			found=1
			print GetOneAddress(initialPage[parent.position:tillindex])
		else:
			parent=parent.parent

# this function tries to find missing day or address nearest to the pattern
def FindMissingInfoInNearbyArea(pattern,day,address):
	txt=browser.page_source	
	if day==1:
		
		missingday= GetMissingDay(txt[0:pattern.start-1])
		print "missing day found"+missingday
		
	elif address==1:
		return GetMissingAddress(txt[0:pattern.start-1])



#for tag in taglist:
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



#browser.get("http://www.birminghamaa.org/meetings.php")#("http://www.aaspringfield.org/Meetings.aspx")"http://aaonmv.org/12step/meeting-schedule/"
#"http://www.aa-waterloo.org/all-meetings.html"
#"http://www.booneaa.org/mondays"
#"http://www.moorecountyaa.org/id2.html"
#"http://www.aajacksonvillenc.org/Pages/AAMeetings.aspx"
#"http://www.aadistrict51.org/Meetings/Meetings.html"
#http://www.aanc32.org/thursday/ 

meetingURLArr=[]
def readMeetingURLs():
	wb = open_workbook('All Meeting Pages_Sabirat.xlsx')
	s=wb.sheets()[0]
	for row in range(1,s.nrows):
		col_value = []
		#for col in range(s.ncols):
		mCity= (s.cell(row,0).value)
		mUrl  = (s.cell(row,1).value)
		mNOM=(s.cell(row,2).value)
		oneMeetingURL=URLInfo(mUrl,mCity,mNOM)
		print mUrl
		
		meetingURLArr.append(oneMeetingURL)


def FindFormWithDaysIfAvailable():
	all_day=["sunday","monday","tuesday","wednesday","thursday","friday","saturday","sun","mon","tues","tue","wed","thurs","thu","fri","sat"]	
	forms=browser.find_elements_by_tag_name("form")
	indexofform=-1
	for form in forms:
		indexofform+=1
		dropdowns=form.find_elements_by_xpath("//select")
		indexofdropdown=-1
		for dropdown in dropdowns:
			indexofdropdown+=1
			day_arr=[]
			options= dropdown.find_elements_by_tag_name("option")
			for option in options:
				probable_day=option.get_attribute("value")
				if probable_day.lower() in all_day:
					day_arr.append(probable_day.lower())
			#print day_arr
			if len(day_arr)>0 and all(x in all_day for x in day_arr):
				FormClass=FormInfo(indexofform,indexofdropdown)
				return FormClass
				
	return None

def FindListWithDaysIfAvailable():
	all_day=["sunday","monday","tuesday","wednesday","thursday","friday","saturday","sun","mon","tues","tue","wed","thurs","thu","fri","sat","any day"]	
	lis=browser.find_elements_by_tag_name("li")
	indexlistarray=[]
	listindex=-1
	for li in lis:
		#print "outside loop"+li.get_attribute('innerHTML')
		listindex+=1
		try:
			href=li.find_element_by_tag_name("a")
			if href:
				probable_day=href.get_attribute('innerHTML')#text
				#print "link found:"+href.get_attribute('innerHTML')
				if probable_day.lower() in all_day:
					indexlistarray.append(listindex)
					#print href.text
		except:
			continue
	print indexlistarray		
	return indexlistarray

def FindRadiosWithDaysIfAvailable():
	all_day=["sun","mon","tues","tue","wed","thu","fri","sat"]	
	forms=browser.find_elements_by_tag_name("form")
	indexofform=-1
	for form in forms:
		indexofform+=1
		formtext=form.get_attribute("outerHTML").lower()
		for oneday in all_day:
			if oneday not in formtext:
				print formtext
				print oneday
				return None
	FormClass=FormInfo(indexofform,0)
	return FormClass
				
	return None
'''the last 3 parameters are passed beforehead if the pattern has missing information according to PD algo'''
def ExtractMeetingInfo(mPattern,fulltext,mDay,mTime,mAddress):
	if not mTime:	
		mTime=GetMeetingTime(RemoveHTMLTags(fulltext))
	if not mAddress:
		mAddress=GetMeetingAddress(RemoveHTMLTags(fulltext))
	if not mDay:	
		mDay=GetMeetingDay(RemoveHTMLTags(fulltext))
	'''if mTime and mDay and mAddress:	
		#print "Time:"+mTime+", Day:"+mDay+",Address:"+mAddress#+"text:"+RemoveHTMLTags(fulltext)
		#print "outside function"+fulltext
		mPos=FindMeetingXY(mPattern,fulltext,mDay,mTime,mAddress)'''
	mPos=FindMeetingXY(mPattern,fulltext,mDay,mTime,mAddress)
			

'''this function mainly runs the pattern detection algorithm and call ExtractMeetingInfo() for each probable meeting pattern '''
def LoadPagesAndRunPD(dayInfo):
	txt=browser.page_source	#browser.find_element_by_tag_name('html').get_attribute('outerHTML')
	'''txt=txt.replace("&nbsp;"," ")
	with codecs.open ("examplePage.html", "w",encoding='utf-8') as myfile:
	    myfile.write(txt)
	txt=txt.replace("%20"," ")'''	


	pagetext=txt#readPageInString("examplePage.html")
	#pagetext=txt
	initialPage=txt#pagetext
	troot=TreeNode("root")
	current=troot
	FindTags(pagetext,current)
	allPatterns=SetSubtrees(troot)
	taglist=FindDuplicates(troot)
	newlist = sorted(taglist, key=lambda x: x.seqcount, reverse=True)

	t=1
	for p in newlist:
		print p.seqstring
		if t==mptc:
			break
		t+=1

	maxweight=0
	maxindex=-1
	i=0
	for tag in taglist:
		if tag.seqcount*.9+tag.tagnums*0.1>maxweight:
			maxweight=tag.seqcount*.9+tag.tagnums*0.1
			maxindex=i
		i+=1



	dcount=0
	for onerecord in newlist:
		for pattern in allPatterns:
			if pattern.patString==onerecord.seqstring and onerecord.tagnums>5:
				#break
				target = open("testhtml.html", 'a')
				withtags=initialPage[pattern.start:pattern.end]
				#tagsArray=strip_tags(withtags)
				#bingo=RemoveHTMLTags(withtags)
				numTime=GetNumberOfTimes(withtags,onerecord.seqcount)
				numAddress=GetNumberOfAddresses(withtags,onerecord.seqcount)


				daytopass=""
				addresstopass=""
				timetopass=""

				if dayInfo:
					numDay=1
					#print "day from dropdown"+dayInfo
					daytopass=dayInfo
				else:				
					numDay=GetPresenceOfDays(withtags,onerecord.seqcount)
				
				#print "Address:"+str(numAddress)+"Time:"+str(numTime)+"Day:"+str(numDay)		
				if numTime>0.2 and numAddress>0.2 and numDay>0.4:
					'''target.write(initialPage[pattern.start:pattern.end])
					target.write("<br>")'''
					ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],daytopass,timetopass,addresstopass)
					HighlightMeeting(pattern,initialPage)
					#HighlightMeeting(pattern,initialPage)
					#mPos=FindMeetingXY(pattern,initialPage)
				elif numTime>0.2 and numAddress>0.02 and numDay==0:					
					#HighlightMeeting(pattern,initialPage)
					#FindMeetingXY(pattern,initialPage)
					#mPos=ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],"","","")
					if dayInfo:
						dayfound=FindMissingInfoInNearbyArea(pattern,1,0)
					else:
						dayfound=dayInfo
					ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],dayfound,timetopass,addresstopass)
					HighlightMeeting(pattern,initialPage)
				'''elif numTime>0.2 and numAddress>0.01 and numDay==0:
					target.write("<tr>Missing Day:"+GetMissingDay(initialPage[0:pattern.start-1])+"</tr>")
					target.write("<br><br>")			
					target.write(initialPage[pattern.start:pattern.end])
					target.write("<br><br><br>")
					HighlightMeeting(pattern,initialPage)'''
				
readMeetingURLs()

'''loads all the meeting web pages, find out if dropdown/link of days are available, clicks through all of them'''
for oneURL in meetingURLArr:
	browser.get("http://www.aastpaul.org/?topic=8")#("http://aaminneapolis.org/meetings/?d=1&v=list")#("http://www.aadistrict1.org/page7.php")#("http://aaminneapolis.org/meetings/?d=any&v=list")#(oneURL.urlString)#"http://aaminneapolis.org/meetings/?d=any&v=list"
	formfound=FindFormWithDaysIfAvailable()
	listfound=FindListWithDaysIfAvailable()
	radiofound=FindRadiosWithDaysIfAvailable()
	if formfound:
		forms=browser.find_elements_by_tag_name("form")
		dropdowns=forms[formfound.formelement].find_elements_by_xpath("//select")
		options=dropdowns[formfound.dropdownelement].find_elements_by_tag_name("option")
		for indexoption in range(0,len(options)-1):
			dayinfo=options[indexoption].get_attribute("value")			
			options[indexoption].click()
			forms[formfound.formelement].submit()
			
			forms=browser.find_elements_by_tag_name("form")
			dropdowns=forms[formfound.formelement].find_elements_by_xpath("//select")
			options=dropdowns[formfound.dropdownelement].find_elements_by_tag_name("option")
			print "day---"+dayinfo
			LoadPagesAndRunPD(dayinfo)
	elif len(listfound)>0:
		lis=browser.find_elements_by_tag_name("li")
		for indexoption in range(0,len(listfound)-1):
			try:
				element=lis[listfound[indexoption]].find_element_by_tag_name("a")
				print element.get_attribute("innerHTML")
				if element:
					dayinfo=element.get_attribute("innerHTML")
					browser.execute_script("arguments[0].click();", element)
					lis=browser.find_elements_by_tag_name("li")
					print "day found---"+dayinfo
					LoadPagesAndRunPD(dayinfo)
			except Exception as e:
				print e
				continue
	elif len(browser.find_elements_by_tag_name("form"))>0:
		beforeurl=browser.page_source
		forms=browser.find_elements_by_tag_name("form")
		lform=len(forms)
		for i in range(0,lform):
			browser.find_elements_by_tag_name("form")[i].submit()
			LoadPagesAndRunPD(None)
			browser.get(beforeurl)
	else:
		print "in else"
		LoadPagesAndRunPD(None)
	break
	
			







