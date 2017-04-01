import time
import threading
import sqlite3
from bs4 import BeautifulSoup

class DTThread(threading.Thread):
	

	def __init__(self, work_queue):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
	
	def run(self):
		while True:
			#table = 'trumptower'
			#conn = sqlite3.connect('db/data.db')
			#c = conn.cursor()
			#c.execute('''DROP table trumptower''')
			#c.execute('''CREATE TABLE 
			#	IF NOT EXISTS trumptower (TEXT data)''')
			trump_data = self.work_queue.get()
			
			#print(data)
			soup = BeautifulSoup(trump_data, 'html.parser')

			#column = "data"
			#title = soup.title.string
			#print("Aggregating " + title)

			#query = "INSERT INTO trumptower ('{:s}') VALUES ('{:s}')".format(column,title)
			#print(query)
			#c.execute(query)
			#conn.commit()

			#c.execute("SELECT data FROM trump")
			#print(c.fetchall())
			#conn.close()
			#print(soup.prettify().encode('UTF-8'))
			self.work_queue.task_done()
			time.sleep(5)
