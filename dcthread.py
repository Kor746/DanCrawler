import threading
import queue
import time
import logging
import urllib
from urllib.request import urlopen
from robotparser import RobotFileParser

#This class runs multiple jobs for grabbing the urls
class DCThread(threading.Thread):
	
	def __init__(self, load_queue, work_queue):
		threading.Thread.__init__(self)
		self.load_queue = load_queue
		self.work_queue = work_queue 

	# invoked implicitly by thread
	def run(self):
		while True:
			#Get link from load queue
			link = self.load_queue.get()

			#Get data from link
			data = self.loadLink(link)
			
			#Put data in work queue
			self.work_queue.put(data)

			#Signal load_queue task done 
			self.load_queue.task_done()

	#Load the content of the urls
	def loadLink(self, link):
		try:
			if (self.readRobots(link.getName()) == True) and (urlopen(link.getUrl()).getcode() == 200):
				print("Crawling..." + link.getUrl() + " From " + link.getName())
				return urlopen(link.getUrl()).read()
		except urllib.error.URLError:
			print("Invalid URL: " + link.getUrl())
			pass
		except urllib.error.HTTPError:
			print("HTTP Error! " + link.getUrl())
			pass
		return ""
		
	#Checks robots.txt to see if bots are allowed on webpage
	def readRobots(self, url):
		rp = RobotFileParser()
		link = url + "robots.txt"
		print("Checking..." + link)
		rp.set_url(link)
		rp.read()
		#returns true if allowed, otherwise false
		return rp.can_fetch("*", link)