class Queue:
	def __init__(self):
		self.items = []
		
	def isEmpty(self):
		return self.items == []
		
	def enqueue(self, item):
		#print "enquing page"+item
		self.items.insert(0,item)
		
	def dequeue(self):
		it= self.items.pop()
		#print "dequeing:"+it
		return it
	
	def size(self):
		return len(self.items)
		
	def printqueue(self):
		print(self.items)
