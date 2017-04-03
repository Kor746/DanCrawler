#Model for an article object
class Article:
	title = ""
	content = ""
	def __init__(self, title, content):
		self.title = title
		self.content = content

	def getTitle(self):
		return self.title

	def getContent(self):
		return self.content
