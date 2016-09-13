import collections
import codecs
import time
from classes import PatternString, TreeNode, Sequence, MLStripper, URLInfo, FormInfo
from Features import GetNumberOfTimes, GetNumberOfAddresses, GetPresenceOfDays, GetMissingAddresses, GetMissingDay
from PageFilter import readPageInString, traverse, traversePrint, SetSubtrees, FindDuplicates, FindTags
from MeetingInformationExtractionFunctions import GetMeetingTime, GetMeetingAddress,GetMeetingDay,RemoveHTMLTags
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from xlrd import open_workbook
import string


from BeautifulSoup import BeautifulSoup

browser = webdriver.Chrome()#("C:\Users\Bittamoni\Downloads\chromedriver.exe")
#browser.set_window_size(1180,800)
txt=""
mptc=40	#maxiumum # of patterns to consider
wAddress=0.3
wTime=0.4


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




def HighlightMeeting2(pattern,initialPage):
	first_tag=pattern.patString.split(',')[0]
	pagesubstring= initialPage[pattern.start:pattern.end]
	soup=BeautifulSoup(pagesubstring)
	souptext=soup.text
	filtered_soup = filter(lambda x: x in string.printable, souptext)
	
	for e in browser.find_elements_by_xpath('//'+first_tag+'[contains(text(), "' + pagesubstring + '")]'):#browser.find_elements_by_xpath(".//"+first_tag+"[contains(text(), \""+soup.text+"\")]"):
		highlight(e)
		continue
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

def FindInfoInParents(cNode,tillindex):
	parent=cNode.parent
	found=0
	cnt=0
	while not found:
		if cnt==5:
			break
		cnt+=1
		if GetNumberOfAddresses(initialPage[parent.position:tillindex])==1:
			print "one address"
			print cNode.tagname
			found=1
			print GetOneAddress(initialPage[parent.position:tillindex])
		else:
			parent=parent.parent


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
			print day_arr
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

'''the last 3 parameters are passed beforehead if the pattern has missing information according to PD algo'''
def ExtractMeetingInfo(mPattern,fulltext,mDay,mTime,mAddress):
	if not mTime:	
		mTime=GetMeetingTime(RemoveHTMLTags(fulltext))
	if not mAddress:
		mAddress=GetMeetingAddress(RemoveHTMLTags(fulltext))
	if not mDay:	
		mDay=GetMeetingDay(RemoveHTMLTags(fulltext))
	if mTime and mDay and mAddress:	
		print "Time:"+mTime+", Day:"+mDay+",Address:"+mAddress#+"text:"+RemoveHTMLTags(fulltext)
	
			

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
			if pattern.patString==onerecord.seqstring:
				#break
				target = open("testhtml.html", 'a')
				withtags=initialPage[pattern.start:pattern.end]
				#tagsArray=strip_tags(withtags)
				#bingo=RemoveHTMLTags(withtags)
				numTime=GetNumberOfTimes(withtags,onerecord.seqcount)
				numAddress=GetNumberOfAddresses(withtags,onerecord.seqcount)
				numDay=GetPresenceOfDays(withtags,onerecord.seqcount)
				#print "Address:"+str(numAddress)+"Time:"+str(numTime)+"Day:"+str(numDay)		
				if numTime>0.2 and numAddress>0.2 and numDay>0.4:
					'''target.write(initialPage[pattern.start:pattern.end])
					target.write("<br>")'''
					ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],"","","")
					HighlightMeeting2(pattern,initialPage)
				elif numTime>0.2 and numAddress>0.02 and numDay==0:					
					HighlightMeeting2(pattern,initialPage)
					ExtractMeetingInfo(pattern, initialPage[pattern.start:pattern.end],"","","")
				'''elif numTime>0.2 and numAddress>0.01 and numDay==0:
					target.write("<tr>Missing Day:"+GetMissingDay(initialPage[0:pattern.start-1])+"</tr>")
					target.write("<br><br>")			
					target.write(initialPage[pattern.start:pattern.end])
					target.write("<br><br><br>")
					HighlightMeeting(pattern,initialPage)'''
				
readMeetingURLs()

'''loads all the meeting web pages, find out if dropdown/link of days are available, clicks through all of them'''
for oneURL in meetingURLArr:
	browser.get("http://www.aadistrict1.org/page7.php")#("http://aaminneapolis.org/meetings/?d=any&v=list")#(oneURL.urlString)#"http://aaminneapolis.org/meetings/?d=any&v=list"
	formfound=FindFormWithDaysIfAvailable()
	listfound=FindListWithDaysIfAvailable()
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
			LoadPagesAndRunPD(dayinfo)
	elif len(listfound)>0:
		lis=browser.find_elements_by_tag_name("li")
		for indexoption in range(0,len(listfound)-1):
			try:
				element=lis[listfound[indexoption]].find_element_by_tag_name("a")
				if elem:
					dayinfo=element.get_attribute("innerHTML")
					browser.execute_script("arguments[0].click();", element)
					lis=browser.find_elements_by_tag_name("li")
					LoadPagesAndRunPD(dayinfo)
			except:
				continue
	else:
		print "in else"
		LoadPagesAndRunPD(None)
	break
	
			






