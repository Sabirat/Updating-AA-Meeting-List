class TreeNode(object):
	tagname=None
	position=-1
	subpages=[]
	children=None							#after applying BFS to the homepages, we get more URLs that we save here
	def __init__(self, data):
        	self.tagname = data
        	self.children = []
	
	def add_child(self, obj):
        	self.children.append(obj)


def traverse(rootnode):
	thislevel = [rootnode]
  	while len(thislevel)>0:
		nextlevel = list()
		for n in thislevel:
			print n.tagname+",",
		
			for c in n.children:
				nextlevel.append(c)
		print
		thislevel = nextlevel


rt=TreeNode("table")
p=TreeNode("tr")
q=TreeNode("tr")
r=TreeNode("tr")
s=TreeNode("tr")
rt.add_child(p)
rt.add_child(q)
rt.add_child(r)
rt.add_child(s)
g=TreeNode("td")
q.add_child(g)
q.add_child(TreeNode("td"))
s.add_child(TreeNode("a"))

traverse(rt)


