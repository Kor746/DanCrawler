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
		self.url = self.url.replace("www.", "")
		return self.url