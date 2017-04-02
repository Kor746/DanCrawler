#This file contains functions that perform CNN queries
import sqlite3

def insertToDB(article):

	conn = sqlite3.connect('db/trump.db',timeout=10)
	c = conn.cursor()

	#c.execute('''DROP TABLE IF EXISTS trump_articles''')
	c.execute('''CREATE TABLE IF NOT EXISTS trump_articles (article_title TEXT, article_content TEXT)''')

	c.execute('''INSERT INTO trump_articles (article_title, article_content) VALUES (?, ?)''', (article.getTitle(), article.getContent()))
	
	conn.commit()
	conn.close()
	getArticles()

def getArticles():

	conn = sqlite3.connect('db/trump.db',timeout=5)
	c = conn.cursor()
	articles = []
	for row in c.execute("SELECT * FROM trump_articles ORDER BY ROWID ASC LIMIT 25"):
		articles.append(row)
		#print(row)
	conn.close()
	return articles