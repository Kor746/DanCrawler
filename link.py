# Link class
class Link:
	
	name = ""
	url = ""
	def __init__(self, name, url):
		self.name = name
		self.url = url

	def getName(self):
		return self.name

	def getUrl(self):
		return self.url