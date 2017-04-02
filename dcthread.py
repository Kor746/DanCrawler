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
			#If robots.txt and status code of url is good then we can get the content
			if (self.readRobots(link.getName()) == True) and (urlopen(link.getUrl()).getcode() == 200):
				#print("Getting..." + link.getUrl() + " FROM..." + link.getName())
				return urlopen(link.getUrl()).read()
		except urllib.error.URLError:
			print("Invalid URL: " + link.getUrl())
			pass
		except urllib.error.HTTPError:
			print("HTTP Error! " + link.getUrl())
			pass
		return ""
		
	#Checks urls robots.txt to see if bots are allowed on webpage
	def readRobots(self, url):
		robot_url = url + "robots.txt"
		rp = RobotFileParser()
		#Checks trusted_links.txt to see if it the url provided is already trusted
		with open('trusted_links.txt', 'r') as f:
			read_data = f.readlines()
			for line in read_data:
				#print("Looking for..." + robot_url)
				if line.rstrip('\n') == robot_url:
					return True
		#If the url was not found in the file then we check the robot.txt
		f.close()
		rp.set_url(robot_url)
		rp.read()
		rp_flag = rp.can_fetch("*", robot_url)
		#If checking return true then we can write into the file as a trusted link
		#It is recommended to check the robot.txt and write it into the file yourself
		if rp_flag == True:
			o = open('trusted_links.txt', 'a')
			o.write(robot_url + '\n')
			o.close()
			return True
		return False