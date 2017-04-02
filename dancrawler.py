# Name: DanCrawler
# Author: Daniel Lee
# Date: March 30, 2017
# E-mail: danlee746@hotmail.ca
# Version: Python 3.4.1
# Purpose: This web crawler is meant to retrieve top 25 articles 
# and tweets about Donald Trump. Make Crawling Great Again! (MCGA)

import queue
import threading
import time
import sys
import json
import sqlite3
import twitterdb
#Stores Twitter keys
import config
import tweepy
from tweepy import OAuthHandler
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from dcthread import DCThread
from dtthread import DTThread
from link import Link
from tweet import Tweet
########### Suggestion #############
#We can also use grequests to get send url req's async, but I will use threading for my app
#https://github.com/kennethreitz/grequests
#import grequests

#This is the query url for top 25 Donald Trump stories...but I guess stories aren't really articles?
#http://searchapp.cnn.com/search/query.jsp?page=1&npp=25&start=1&text=Donald%2BTrump&type=all&bucket=true&sort=date&collection=STORIES&csiID=csi4
cnn_url = 'http://cnn.com'
twitter_user ='realDonaldTrump'
num_tweets = 25

#The Q's
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
			tweet_data.append(tweet._json)
		return tweet_data
	except tweepy.TweepError:
		print("Error getting twitter data!")
		pass
	return tweet_data
	
def parseTwitterData():
	#Iterates json dict, creates a tweet object and passes to insert to db func
	the_data = getTwitterData()
	if len(the_data) != 0:
		for tweet_data in the_data:	
			#Constructing tweet obj with text and date attributes	
			tweet = Tweet(str(tweet_data['text'].encode('utf-8')).strip(),
				str(tweet_data['created_at'].encode('utf-8')).strip())
			twitterdb.insertToDB(tweet)
	else: 
		print("Error getting twitter data!")
			
def parseCNNData():
	url_data = getCNNData()
	soup = BeautifulSoup(url_data, 'html.parser')
	cnn_data = soup.findAll("script")
	#Cleaning and parsing the ResultSet strings
	clean_cnn = str(cnn_data[8]).split(', siblings:         ')[1]
	clean_cnn = clean_cnn.split('                     , registryURL:')[0]
	clean_cnn = json.loads(clean_cnn)
	clean_cnn = clean_cnn['articleList']

	links = []
	for link in clean_cnn:
		full_link = cnn_url + link['uri']
		link = Link(cleanUrl(full_link), full_link)
		links.append(link)
	return links

def getCNNData():
	try:
		if urlopen(cnn_url).getcode() == 200:
			return urlopen(cnn_url).read()
	except urllib.error.URLError:
		print("Invalid URL: " + cnn_url)
		pass
	except urllib.error.HTTPError:
		print("HTTP Error! " + cnn_url)
		pass
	return ""
	
#Cleans up url and returns the root hostname.com... got sidetracked lol
def cleanUrl(url):
	if ('http' in url) or ('https' in url):
		url = url.replace("/", ".")
		if 'com' == url.split('.')[3]:
			return url.split('.')[0] + '//' + url.split('.')[2] + '.com/'	
		return url.split('.')[0] + '//' + url.split('.')[3] + '.com/'
	return print("Please append http or https to " + url)


#Start program timer
start_time = time.time()
def main():
	links = parseCNNData()

	#Number of slaves muahahahaha :)
	#Too slow? You must construct additional threads!!
	num_threads = 12
	
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

	print("Grabbing Trump Tweets...")
	parseTwitterData()	

	#Blocks until items are processed
	load_queue.join()
	work_queue.join()

#Program entry 
__name__ = '__main__'

#Call main func to start program
main()

#Current time - start time =  elapsed time
print("Elapsed Time = " + str(time.time() - start_time))