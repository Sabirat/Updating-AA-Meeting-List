
class CityURL(object):
    cityname=None
    cityaaurl=None
    subpages=[]								#after applying BFS to the homepages, we get more URLs that we save here
    def __init__(self, cname,url):
        self.cityname = cname
	self.cityaaurl=url

    def getCity(self):
        return self.cityname

    def getCityAAURL(self):
        return self.cityaaurl
	
    def setSubpages(self,arrayofurl):
	this.subpages=arrayofurl



class URLbyState(object):						#contains URLs and text of pages and other information of a state
    
    cities=[]
    name=[]
    def __init__(self, name,city_array):
        self.name = name
	self.cities=city_array

    def getName(self):
        return self.name

    def getCities(self):
        return self.Cities
	
