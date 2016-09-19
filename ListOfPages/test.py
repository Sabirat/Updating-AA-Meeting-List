from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import  requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time ,os ,re
from HelperFunctions import IsValidWebpage


url="http://www.nemdaa.org/"
browser = webdriver.Chrome("C:\Users\Bittamoni\Downloads\chromedriver.exe")
browser.get(url)
'''links=browser.find_element_by_tag_name("form")
links.submit()'''
LINK_XPATH = '//*[@href or @src]'
links = browser.find_elements_by_xpath(LINK_XPATH)
for link in links:
	page=""
	if link.get_attribute("href"):
		page=link.get_attribute("href")
	elif link.get_attribute("src"):
		page=link.get_attribute("src")
	print page
	print IsValidWebpage(page,url,"")
	
	
	
	
'''print links[i].get_attribute("href")
ref=links[i].get_attribute("href")
browser.get(ref)
l2=browser.find_elements_by_tag_name("a")
for l in l2:
	print l.get_attribute("href")'''
	
'''submit_BUTTON_XPATH = '//*[@type="submit"]'
buttons = browser.find_elements_by_xpath(submit_BUTTON_XPATH)
for index in range(len(buttons)):
	if buttons[index].is_displayed():
		buttons[index].click()
	try:
		browser.switch_to_alert().accept()
	except:
		pass
	print browser.current_url
	browser.back()
	print "browser back"
	print browser.current_url
	buttons = browser.find_elements_by_xpath(submit_BUTTON_XPATH)'''
'''submit_BUTTON_XPATH = '//*[@href or @src]'
button = browser.find_elements_by_xpath(submit_BUTTON_XPATH)
for b in button:
	if b.get_attribute("href"):
		print b.get_attribute("href")
	if b.get_attribute("src"):
		print b.get_attribute("src")'''
	
'''if not os.path.exists("../alsd"):
    os.makedirs("../alsd")
url="http://aahuntsvilleal.com/wp-content/uploads/2016/06/FullOpen.pdf"
browser = webdriver.Chrome()
browser.get(url)
print browser.page_source
print(requests.head(url).headers["Content-Type"])
links=browser.find_elements_by_tag_name("a")
for link in links:
	print link.get_attribute("href")
'''
'''
browser = webdriver.Chrome()
browser.get("http://www.birminghamaa.org/meetings.php?day=SUN")
submit_BUTTON_XPATH = '//input[@type="submit"]'
button = browser.find_element_by_xpath(submit_BUTTON_XPATH)
if button is not None:	
	button.click()
	#txt=browser.page_source
	#print txt
	#fo = open("meetingtext.html", "wb")
	#fo.write(txt)
	print "form found"
	print browser.current_url
'''
'''url=[]
browser = webdriver.Chrome("C:\Users\Bittamoni\Downloads\chromedriver.exe")
wait = WebDriverWait(browser, 3)
browser.get("http://www.birminghamaa.org/meetings.php?day=SUN")
WebDriverWait(browser, 3).until(EC.presence_of_element_located(browser.find_element_by_tag_name('a')))
links=browser.find_elements_by_tag_name("a")
print browser.page_source'''
'''for page in links:
	href=page.get_attribute("href")
	
	if  href and "www.aa.org" not in href and not href.endswith(".js") and not href.endswith(".css"):
		url.append(href)

for onehref in url:
	browser.get(onehref)'''

'''
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

'''
#print convert('pdfs example/When_and_Where.pdf',[0,0])

