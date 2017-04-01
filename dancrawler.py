# Name: DanCrawler
# Author: Daniel Lee
# Date: March 30, 2017
# E-mail: danlee746@hotmail.ca
# Version: Python27
# Purpose: This web crawler is meant to retrieve top 25 articles 
# and tweets about Donald Trump. Make Crawling Great Again!

import queue
import threading
import time
import sys
import json
import sqlite3
#Stores Twitter keys
import config
import tweepy
import numpy as np
from tweepy import OAuthHandler
#import newspaper3k
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from dcthread import DCThread
from dtthread import DTThread
from link import Link

########### Suggestion #############
#We can also use grequests to get send url req's async, but I will use threading for my app
#https://github.com/kennethreitz/grequests
#import grequests



#'http://searchapp.cnn.com/search/query.jsp?page=1&npp=25&start=1&text=Donald%2BTrump&type=all&bucket=true&sort=date&collection=STORIES&csiID=csi4'
cnn_url = 'http://cnn.com'
twitter_user ='realDonaldTrump'
num_tweets = 25
#Queue variables
load_queue = queue.Queue()
work_queue = queue.Queue()

def getTwitterData():
	#OAuth access authentication
	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_token_secret)
	api = tweepy.API(auth)
	#List to store tweets
	tweet_data = []
	try:
		for tweet in api.user_timeline(screen_name = twitter_user, count = num_tweets):
			tweet_data.append(json.dumps(tweet._json))
			#tweet_data.append(tweet.text.encode('utf-8'))
			#print(tweet.text.encode('utf-8'))
	except tweepy.TweepError:
		print("Error getting tweet")
		time.sleep(10)
		pass

	return tweet_data

def parseTwitterData():
	tweet_data = []
	tweet_date = []
	for tweets_obj in getTwitterData():
		tweet_dict = json.loads(tweets_obj)
		for topic,tweet in tweet_dict.items():
			if topic == 'text':
				tweet_data.append(tweet.encode('utf-8'))
			if topic == 'created_at':
				tweet_date.append(tweet.encode('utf-8'))
	
	tweet_array = np.column_stack((tweet_data, tweet_date))
	print(tweet_array)	
	
	#tweets = []
	#[tweets.append(i) for i in tweet_data]
	#print(tweets)
	#for i in tweets:
	#	print(i.encode('utf-8'))
	
		
	

def parseCNNData():
	cnn_articles = newspaper3k.build('http://cnn.com')

	for article in cnn_articles.articles:
		print(article.url['text'])
	#url_data = readCNNUrl()
	
	#soup = BeautifulSoup(url_data, 'html.parser')

	#cnn_data = soup.find("textarea")
	#cnn_content = str(cnn_data.contents[0])
	
	# load string to json object (dict)
	#cnn_json = json.loads(cnn_content)
	#print(cnn_json)
	#print(json.dumps(cnn_json, indent = 4))


def readCNNUrl():
	try:
		status_code = urlopen(cnn_url).getcode()
		if status_code == 200:
			cnn_data = urlopen(cnn_url).read().decode('UTF-8')
			return cnn_data
	except urllib.error.URLError:
		print("Invalid URL: " + link.getUrl())
		pass
	except urllib.error.HTTPError:
		print("HTTP Error!")
		pass
	return ""
	

#Cleans up url and returns the root hostname.com
def cleanUrl(url):
	if ('http' in url) or ('https' in url):
		url = url.replace("/", ".")
		if 'com' == url.split('.')[3]:
			return url.split('.')[0] + '//' + url.split('.')[2] + '.com/'	
		return url.split('.')[0] + '//' + url.split('.')[3] + '.com/'
	return print("Please append http or https to " + url)


#Start timer
start_time = time.time()
def main():
	parseTwitterData()
	link = Link(cleanUrl('http://blah.com'), 'http://blah.com')
	links = [link]
	#Number of slaves muahahahaha
	num_threads = 4
	#Too slow? You must construct additional threads!!

	#Loading the load_queue with links
	for link in links:
		load_queue.put(link)

	for i in range(num_threads):
		#creating a DanCrawler thread instance with 2 queues
		dcthread = DCThread(load_queue, work_queue)
		dcthread.setDaemon(True)
		#print("DanCrawler thread " + str(i + 1) + " starting...")
		dcthread.start()

	for i in range(num_threads):
		dpthread = DTThread(work_queue)
		dpthread.setDaemon(True)
		#print("Data process thread " + str(i + 1) + " starting...")
		dpthread.start()
	
	#Blocks until items are processed
	load_queue.join()
	work_queue.join()

#Program entry 
__name__ = '__main__'
#Call main func to start program
main()
#Current time - start time =  elapsed time
print("Total Time = " + str(time.time() - start_time))