#This file contains functions that perform CNN queries
import sqlite3

def insertToDB(articles):
	conn = sqlite3.connect('db.sqlite3', timeout=5)
	c = conn.cursor()
	#c.execute('''DROP TABLE IF EXISTS crawlapp_trump_articles''')
	c.execute('''CREATE TABLE IF NOT EXISTS crawlapp_trump_articles 
		(id INTEGER PRIMARY KEY,
		article_title TEXT NOT NULL, 
		article_content TEXT NOT NULL)''')	

	for article in articles:
		c.execute('''INSERT INTO crawlapp_trump_articles(article_title, article_content) VALUES(?,?)''', (article.getTitle(),article.getContent()))
	
	conn.commit()
	conn.close()
	
	
#Testing if articles saved to the table
def getArticles():
	conn = sqlite3.connect('db.sqlite3', timeout=5)
	c = conn.cursor()
	articles = []
	for row in c.execute("SELECT * FROM crawlapp_trump_articles LIMIT 25"):
		articles.append(row)
	conn.close()
	return articles