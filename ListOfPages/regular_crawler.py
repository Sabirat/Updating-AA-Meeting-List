from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time ,os ,re ,urllib ,Queue

class web_crawl(object):
	fd = 0
	output = 0
	url_list = []
	


	def __init__(self,path,output_path):
		self.fd = open(path,'r')
		self.output = open(output_path,'a')


	def read_file(self):
		while 1:
			line = self.fd.readline()
			if not line :
				break
			elif line != '':
				self.url_list.append(line)
	
	def crawling_static(self , url):
		init_page = "http://www.gulfcoastaa.org"
		url_set = set()
		url_queue = Queue.Queue()
		url_queue.put(init_page)
		lst = []
		while url_queue.empty() != True:
			cur_url = url_queue.get()
			if cur_url in url_set:
				continue
			url_set.add(cur_url)
			print cur_url
			try:
				webpage = urllib.urlopen(cur_url)
			except IOError:
				pass
			for data in webpage:
				count = 0 
				data = data.strip()
				self.output.write(data)
				if re.match('.*href*',data):
					count = count + 1
					#new_page = data.split('\"')
					new_page = data[data.find('http'):]
					new_page = new_page[0:new_page.find('\"')]
					print "newpage = " + new_page
					if new_page != "" and count <= 3:
						url_queue.put(new_page)
						count = 0;
					
			
			for web in lst:
				print web

	def start(self):
		self.read_file()
		for url in self.url_list:
			self.crawling_static(url)

		
				




if __name__ == "__main__":
	crawl = web_crawl("output.txt","crawling.html")
	crawl.start()


	








	
