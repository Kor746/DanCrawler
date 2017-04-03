#This file contains functions that perform Twitter queries
import sqlite3

def insertToDB(tweets):
	conn = sqlite3.connect('db.sqlite3', timeout=5)
	c = conn.cursor()
	#c.execute('''DROP TABLE IF EXISTS crawlapp_trump_tweets''')
	c.execute('''CREATE TABLE IF NOT EXISTS crawlapp_trump_tweets 
		(id INTEGER PRIMARY KEY,
		tweet_text TEXT NOT NULL, 
		tweet_date TEXT NOT NULL)''')

	for tweet in tweets:
		c.execute('''INSERT INTO crawlapp_trump_tweets(tweet_text, tweet_date) VALUES(?,?)''', (tweet.getText(),tweet.getDate()))
	
	conn.commit()
	conn.close()

def getTweets():
	conn = sqlite3.connect('db.sqlite3', timeout=5)
	c = conn.cursor()
	tweets = []
	for row in c.execute("SELECT * FROM crawlapp_trump_tweets LIMIT 25"):
		tweets.append(row)
	conn.close()
	return tweets
