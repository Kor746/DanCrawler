# Name: DanCrawler
# Author: Daniel Lee
# Date: March 30, 2017
# E-mail: danlee746@hotmail.ca
# Version: Python27
# Purpose: This web crawler is meant to find top 25 articles and tweets about Donald Trump

import queue
import threading
import time
import sys
import json
#We can also use grequests to get send url req's async, but I will use threading for my app
#https://github.com/kennethreitz/grequests
#import grequests
from urllib.request import urlopen
import urllib
from dthread import DThread
from link import Link
from robotparser import RobotFileParser


#Queue variables
load_queue = queue.Queue()
work_queue = queue.Queue()

path = 'links/links.txt'

#This class runs multiple jobs for grabbing the urls
class DanCrawler(threading.Thread):

	
	def __init__(self, load_queue, work_queue):
		threading.Thread.__init__(self)
		self.load_queue = load_queue
		self.work_queue = work_queue 

	# invoked implicitly by thread
	def run(self):
		while True:
			# get links from queue
			link = self.load_queue.get()
			
		
			data = self.loadLink(link)
			
			
			self.work_queue.put(data)

			# load_queue task done
			self.load_queue.task_done()
			time.sleep(5)




	def loadLink(self, link):
		if self.readRobots(link.getName()) == True:
			statusCode = 0
			print("Extracting " + link.getUrl() + " from...." + link.getName())
			try:
				statusCode = urlopen(link.getUrl()).getcode()
			except urllib.HTTPError:
				if statusCode != 200:
					print("Error: " + err)

			if statusCode == 200:
				return urlopen(link.getUrl()).read().decode('UTF-8')
			else:
				print("Error: " + str(statusCode) + "Retrying..")
				time.sleep(5)
				return ""
		return ""
		
	#Checks robots.txt to see if bots are allowed
	def readRobots(self, url):
		rp = RobotFileParser()
		link = url + "robots.txt"
		print(link)
		rp.set_url(link)
		rp.read()
		return rp.can_fetch("*", link)


def readFile(path):
	links = []
	with open(path, 'r') as f:
		data = f.read().splitlines()
		for line in data:
			if (line != "") and (cleanUrl(line)) != "":
				link = Link(cleanUrl(line), line)
				links.append(link);
			else:
				print("Please append http or https to link!!! " + line)
	f.closed
	return links

def cleanUrl(url):
	if ('http' in url) or ('https' in url):
		url = url.replace("/", ".")
		if url.split('.')[4] != 'com':
			return url.split('.')[0] + '//' + url.split('.')[4] + '.com/'
		return url.split('.')[0] + '//' + url.split('.')[3] + '.com/'
	return ""

	

#Start timer
start_time = time.time()

def main():
	links = readFile(path)
	num_threads = 1
	#Putting my slaves to work
	
	for link in links:
		load_queue.put(link)

	for i in range(num_threads):
		thread = DanCrawler(load_queue, work_queue)
		thread.setDaemon(True)
		thread.start()
		print("Load thread " + str(i + 1) + " starting...")



	for i in range(num_threads):
		dthread = DThread(work_queue)
		dthread.setDaemon(True)
		dthread.start()
		print("Data thread " + str(i + 1) + " starting...")

	#Join threads after processing

	load_queue.join()
	work_queue.join()

__name__ = '__main__'
main()
print("Total Time = " + str(time.time() - start_time))