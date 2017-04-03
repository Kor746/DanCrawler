from django.db import models

# Create your models here.
class Trump_Tweets(models.Model):
	tweet_text = models.TextField()
	tweet_date = models.TextField()

	def __str__(self):
		return self.tweet_text

	def get_date(self):
		return self.article_date

class Trump_Articles(models.Model):
	article_title = models.TextField()
	article_content = models.TextField()

	def __str__(self):
		return self.article_title

	def get_content(self):
		return self.article_content
	