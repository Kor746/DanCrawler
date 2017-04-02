#This file contains functions that perform Twitter queries
import sqlite3

def insertToDB(tweet):
	conn = sqlite3.connect('db/trump.db',timeout=5)
	c = conn.cursor()

	c.execute('''DROP TABLE IF EXISTS trump_tweets''')
	c.execute('''CREATE TABLE IF NOT EXISTS trump_tweets (tweet_text TEXT, tweet_date TEXT)''')
	
	c.execute('''INSERT INTO trump_tweets (tweet_text, tweet_date) VALUES (?, ?)''', (tweet.getText(),tweet.getDate()))
	
	conn.commit()
	conn.close()

def getTweets():
	conn = sqlite3.connect('db/trump.db',timeout=5)
	c = conn.cursor()
	tweets = []
	for row in c.execute("SELECT * FROM trump_tweets ORDER BY ROWID ASC LIMIT 25"):
		tweets.append(row)
	
	conn.close()
	return tweets
