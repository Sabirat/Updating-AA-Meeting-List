# Updating-AA-Meeting-List

1. The first step is to scrape aa.org and locate all local AA websites. The list of the websites with corresponding district names have been saved as XML (AAhomepages.py and it creates AllAAHomePages.xml)
2. In ListOfPages directory, there is newcopy.py that parses this XML, go through all the webpages and uses a level-order traversal technique to find out all the links and buttons available. This repeats for three levels of links. This file saves all of these pages with feature vectors to classify the pages as meeting pages or not. We have five features for this algorithm:
	a) # of times
	b) # of addresses
	c) If all 7 days are present
	d) Count of the word meeting in page
	e) Count of the word meeting in url
These pages and features are saved as spreadsheets for latter stages of the pipeline (See the shared Google Drive folder:States)
3. Using WEKA the pages are classified as 0 or 1 (to be added later)
4. The directory Pattern Detection 9th Sept contains codes for the pattern detection algorithm to detect single meeting from meeting list and save the information to database (treenode.py)
