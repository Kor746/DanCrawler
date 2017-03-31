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
#We can also use grequests to get send url req's async, but I will use threading for my app
#https://github.com/kennethreitz/grequests
#import grequests
from urllib.request import urlopen
from dthread import DThread
from link import Link
from robotparser import RobotFileParser


#Queue variables
load_queue = queue.Queue()
work_queue = queue.Queue()

path = 'links/links.txt'

#This class runs multiple jobs for grabbing the urls
class DanCrawler(threading.Thread):

	robots_flag = False
	

	def __init__(self, load_queue, work_queue):
		threading.Thread.__init__(self)
		self.load_queue = load_queue
		self.work_queue = work_queue 

	# invoked implicitly by thread
	def run(self):
		while True:
			# get links from queue
			link = self.load_queue.get()
			
			data = self.loadUrl(link)

			
			self.work_queue.put(data)

			# load_queue task done
			self.load_queue.task_done()
			time.sleep(5)


	#def exception_handler(self, request, exception):
	#	print("The request " + request + " failed because: " + exception)

	def loadUrl(self, link):
		if self.readRobots(link.getUrl()) == True:
			print("Extracting " + link.getUrl() + " from...." + link.getName())
			return urlopen(link.getUrl()).read().decode('UTF-8')
		
			#Can use this as an alternative to threads. This actually may be faster!
			#req = grequests.get(links.getUrl(), timeout = 0.001)
			#Sends all requests at the same time
			#grequests.map(req, exception_handler=self.exception_handler)

		return print("Error: Robot.txt policy rejection!")
		
	#Checks robots.txt to see if bots are allowed
	def readRobots(self, url):
		rp = RobotFileParser()
		rp.set_url(url + "robots.txt")
		rp.read()
		return rp.can_fetch("*", url)

def readFile(path):
	links = []
	with open(path, 'r') as f:
		data = f.read().splitlines()
		for i in data:
			link = Link(cleanUrl(i), i)
			links.append(link);
		
	f.closed
	return links

def cleanUrl(url):
	http = "http://"
	https = "https://"
	if http in url:
		url = url.replace("http://","")
		return url.split('/')[0]
	elif https in url:
		url = url.replace("https://","")
		return url.split('/')[0]

#Start timer
start_time = time.time()
def main():
	links = readFile(path)
	#Putting my slaves to work
	num_threads = len(links) * 2
	for i in range(num_threads):
		thread = DanCrawler(load_queue, work_queue)
		thread.setDaemon(True)
		thread.start()
		print("Load thread " + str(i + 1) + " starting...")

	for link in links:
		load_queue.put(link)

	for i in range(num_threads):
		dthread = DThread(work_queue)
		dthread.setDaemon(True)
		dthread.start()
		print("Data thread " + str(i + 1) + " starting...")

	#Join threads after processing
	load_queue.join()
	work_queue.join()

main()
print("Total Time = " + str(time.time() - start_time))