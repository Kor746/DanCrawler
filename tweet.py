#A model for a tweet object

class Tweet:
	tweet_text = ""
	tweet_date = ""

	def __init__(self, tweet_text, tweet_date):
		self.tweet_text = tweet_text
		self.tweet_date = tweet_date

	def getText(self):
		return self.tweet_text

	def getDate(self):
		return self.tweet_date