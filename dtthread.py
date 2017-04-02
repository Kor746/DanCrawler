import time
import threading
import cnndb
from article import Article
from bs4 import BeautifulSoup

class DTThread(threading.Thread):

	def __init__(self, work_queue):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
	
	def run(self):
		while True:
			trump_data = self.work_queue.get()
			soup = BeautifulSoup(trump_data, 'html.parser')
			my_content = soup.findAll("div", { "class" : "zn-body__paragraph" })
			
			#This filters out articles without content and articles that aren't about Trump :)
			if ('Trump' in str(my_content)) and (len(my_content) != 0):
				content_dict = { soup.title.string : str(my_content) }
				article = Article(soup.title.string, content_dict[soup.title.string])
				cnndb.insertToDB(article)
						
			self.work_queue.task_done()