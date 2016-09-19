from featuresForMeetingPageOrNot import GetNumberOfTimes,GetNumberOfAddresses,GetPresenceOfDays,GetPresenceOfWordMeeting,GetPresenceOfWordMeetingInURL



########################################################################################################################################
##Given URL string, output the type of the page##
########################################################################################################################################
def FindPageType(pageURL):

	AUDIO_TYPES = ('.mp3','.MP3','.mpa','.MPA','.M4A','.m4a','.flac','.FLAC','.ogg','.OGG','.wav','.WAV','.wma','.WMA')
	VIDEO_TYPES = ('.mp4','.MP4','.avi','.AVI','.wmv','.WMV','.mpg','.MPG','.mpeg','.MPEG')
	if not pageURL:
		return "NULL"
	if any(ext in pageURL for ext in AUDIO_TYPES):
		return "NULL"
	if any(ext in pageURL for ext in VIDEO_TYPES):
		return "NULL"
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
	elif pageURL.lower().endswith(".jpeg".lower()) or pageURL.lower().endswith(".gif".lower()) or pageURL.lower().endswith(".jpg".lower()) or pageURL.lower().endswith(".png".lower()) or pageURL.lower().endswith(".bmp".lower()):
		return "IMAGE"
	elif ".org".lower() in pageURL.lower() or ".com".lower() in pageURL.lower() or ".us".lower() in pageURL.lower() or ".ca".lower() in pageURL.lower() or ".net".lower() in pageURL.lower():
		return "WEBPAGE"
	else:
		return "UNKNOWN"

def SetHeaderOfCSV(list_row):
	list_row.append([])
	list_row[0].append("URL")
	list_row[0].append("page type")
	list_row[0].append("# of times")
	list_row[0].append("#of addresses")
	list_row[0].append("Days present or not")
	list_row[0].append("Meeting In URL present?")
	list_row[0].append("Meeting In Text how many times?")
	list_row[0].append("MeetingOrNot")

def SetARowOfCSV(list_row,page_url,textofpage,ftype):
	rowcount=len(list_row)
	list_row.append([])		
	list_row[rowcount].append(page_url)
	list_row[rowcount].append(ftype)
	list_row[rowcount].append(GetNumberOfTimes(textofpage))
	list_row[rowcount].append(GetNumberOfAddresses(textofpage))
	list_row[rowcount].append(GetPresenceOfDays(textofpage))
	list_row[rowcount].append(GetPresenceOfWordMeetingInURL(page_url))
	list_row[rowcount].append(GetPresenceOfWordMeeting(textofpage))
	#print list_row[rowcount]
	
	
def IsValidWebpage(page,homeurl,urls):
	if not page or not homeurl:
		return False
		
	pagetype=FindPageType(page)
	iswebpage=pagetype is "WEBPAGE" or pagetype is "HTML" or pagetype is "ASP" or pagetype is "PHP"
	if not page:
		return False
		#print anurl+" form page:"+page
		
	hurl=homeurl[0:homeurl.rfind(".")]
	purl=page[0:page.rfind(".")]
	#isindomain=homeurl.replace("www.","").lower() in page.replace("www.","").lower()
	isindomain=hurl.replace("www.","").lower() in purl.replace("www.","").lower()
	#print "home:"+homeurl
	#print "pg:"+page
	if page and page not in urls and iswebpage and "www.aa.org" not in page and isindomain and not ".js" in page.lower() and not ".css" in page.lower() and not "XML".lower() in page.lower():
		return True
	return False
