import collections
import codecs
from classes import PatternString, TreeNode, Sequence, MLStripper
from Features import GetNumberOfTimes, GetNumberOfAddresses, GetPresenceOfDays, GetMissingAddresses, GetMissingDay

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get("http://www.aanc32.org/thursday/")#("http://www.aaspringfield.org/Meetings.aspx")"http://aaonmv.org/12step/meeting-schedule/"
#"http://www.aa-waterloo.org/all-meetings.html"
#"http://www.booneaa.org/mondays"
#"http://www.moorecountyaa.org/id2.html"
#"http://www.aajacksonvillenc.org/Pages/AAMeetings.aspx"
#"http://www.aadistrict51.org/Meetings/Meetings.html"

txt=browser.page_source
txt=txt.replace("&nbsp;"," ")
with codecs.open ("examplePage.html", "w",encoding='utf-8') as myfile:
	    myfile.write(txt)
#txt=txt.replace("%20"," ")	

'''function to traverse in level order'''
def traverse(node):	
	traversalstring=""	
	thislevel = [node]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			#print n.tagname+",",
			traversalstring+=n.tagname+","
		
			for c in n.children:
				nextlevel.append(c)
		#print
		traversalstring+="$$"
		thislevel = nextlevel

	return traversalstring


'''same as traverse but print the nodes'''
def traversePrint(node):
	
	thislevel = [node]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			print n.tagname+",",
			
			for c in n.children:
				nextlevel.append(c)
		print
		thislevel = nextlevel


'''sets all the immediate subnodes of a node. for each node of the trees, 
traverses all it's child nodes and saves these strings as subpages of the node'''
allPatterns=[]										
'''this global list contains all the patterns with their start and 
end position to find out text inside the tags'''
def SetSubtrees(rootnode):
	thislevel = [rootnode]
	while len(thislevel)>0:
		nextlevel = list()

  		for n in thislevel:
			for c in n.children:
				onenode=traverse(c)

				sNode=PatternString(onenode,c.position,c.endposition,c)
				n.subpages.append(sNode)
				allPatterns.append(sNode)
				nextlevel.append(c)
		thislevel = nextlevel



'''def printall(rootnode):
	
	traversalstring=""	
	thislevel = [rootnode]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			print n.tagname
			print n.subpages.patString
		
			for c in n.children:
				nextlevel.append(c)
		print
		
		thislevel = nextlevel'''

'''this function finds all the repetitive patterns in the page'''
def FindDuplicates(rootnode):
	taglist=[]									#list to contain specific patterns and their counts	
	stringlist=[]
	maxim=0
	nd=None
	thislevel = [rootnode]
	cnt=0
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			for child in n.subpages:
							
				cnt=taglist.count(child.patString)
				if child.patString not in stringlist:
					stringlist.append(child.patString)
					OneSeq=Sequence(child.patString,child.patString.count("$"))
					taglist.append(OneSeq)
				else:
					for seq in taglist:
						if seq.seqstring==child.patString:
							seq.seqcount+=1
							break
		
			for c in n.children:
				nextlevel.append(c)
		#print
		
		thislevel = nextlevel

	
	for tg in taglist:
		if tg.seqcount>2 and tg.seqstring.count(",")>5:
			print tg.seqstring
			print tg.seqcount

	'''print maxim
	print nd.tagname
	print tagseq'''
	return taglist
def readPageInString(filename):
	with open (filename, "rb") as myfile:
	    pagetext=myfile.read()

	pagetext=pagetext.lower()
	pagetext=pagetext.replace("<br>"," ")
	pagetext=pagetext.replace("<br/>"," ")
	#pagetext=pagetext.replace("<a","")
	#pagetext=pagetext[500:]
	'''pagetext=pagetext.replace("<abbr>","")
	pagetext=pagetext.replace("</abbr>","")
	pagetext=pagetext.replace("<font","")
	pagetext=pagetext.replace("</font>","")
	pagetext=pagetext.replace("<small","")
	pagetext=pagetext.replace("</small>","")
	pagetext=pagetext.replace("<select","")
	pagetext=pagetext.replace("</select>","")
	pagetext=pagetext.replace("<option","")
	pagetext=pagetext.replace("</option>","")
	pagetext=pagetext.replace("<b>","")
	pagetext=pagetext.replace("</b>","")
	pagetext=pagetext.replace("<i>","")
	pagetext=pagetext.replace("</i>","")
	pagetext=pagetext.replace("<center>","")
	pagetext=pagetext.replace("<hr","")'''
	
	return pagetext


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
		
	


pagetext=readPageInString("examplePage.html")
#pagetext=txt
initialPage=pagetext
troot=TreeNode("root")
i=0
current=troot
while i < len(pagetext):
	if pagetext[i]=='<' and ((pagetext[i+1]>="A" and pagetext[i+1]<="Z") or (pagetext[i+1]>="a" and pagetext[i+1]<="z")):
		if pagetext[i+1]=="b" and pagetext[i+2]=="r" and pagetext[i+3]==">":
			i=i+4
			continue		
		j=i+1
		tag=""
		while pagetext[j]!=">" and pagetext[j]!=" ":
			tag += pagetext[j]
			j+=1
		#print tag
		
		tagnode=TreeNode(tag)
		tagnode.position=i
		current.add_child(tagnode)
		tagnode.set_parent(current)
		current=tagnode

		i=j

	if pagetext[i]=='<' and pagetext[i+1]=="/":
		#print current.tagname
		j=i+2
		endtag=""
		while pagetext[j]!=">":
			endtag += pagetext[j]
			j+=1
		#print "/"+endtag
		
		if current:		
			current.endposition=j+1
			current=current.parent
		i=j

	if pagetext[i]=='/' and pagetext[i+1]==">":
		current.endposition=i		
		i=i+1
		current=current.parent
	i += 1


#traversePrint(troot)
SetSubtrees(troot)
#print troot.children[0].children[0].children[0].tagname
#print troot.children[0].children[0].children[0].subpages
#printall(troot)
taglist=FindDuplicates(troot)
newlist = sorted(taglist, key=lambda x: x.seqcount, reverse=True)


	
maxweight=0
maxindex=-1
i=0
for tag in taglist:
	if tag.seqcount*.9+tag.tagnums*0.1>maxweight:
		maxweight=tag.seqcount*.9+tag.tagnums*0.1
		maxindex=i
	i+=1

#for tag in taglist:
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


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
			if pattern.patString=="span,$$strong,$$font,$$":
				print numAddress		
			if numTime>0.2 and numAddress>0.2 and numDay>0.4:
				target.write(initialPage[pattern.start:pattern.end])
				target.write("<br>")
			elif numTime>0.2 and numAddress==0 and numDay>0.4:
				target.write("<tr>Address:"+GetMissingAddresses(initialPage[0:pattern.start-1])+"</tr>")
				target.write("<br><br>")			
				target.write(initialPage[pattern.start:pattern.end])
				target.write("<br><br><br>")
			elif numTime>0.2 and numAddress>0.01 and numDay==0:
				target.write("<tr>Missing Day:"+GetMissingDay(initialPage[0:pattern.start-1])+"</tr>")
				target.write("<br><br>")			
				target.write(initialPage[pattern.start:pattern.end])
				target.write("<br><br><br>")
			
















