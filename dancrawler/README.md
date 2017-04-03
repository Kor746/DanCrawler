# DanCrawler is an awesome Webcrawler that collects Trump tweets and articles. I created this with Python, Django web framework and sqlite3. I learned Django and sqlite3 while doing it. The only way to learn! I also used multithreading for crawling CNN. 

=================================================================================
!!!MAKE SURE YOU HAVE DJANGO INSTALLED!!!

1. Run 'pip install django' in command shell

2. Run 'python dancrawler.py'. This script will crawl the weblinks for data on Trumpity Trump and update the sqlite3 database.

3. Run 'python manage.py runserver' in the same directory. This should start your server and you can access via localhost:8000 on your browser. Enjoy!

=================================================================================

Afterthoughts:

Hopefully, I can find the time to make the UI prettier, clean up the tweets and articles from tags and escape characters, and deploy it on a hosted server. I tried using heroku's free service, but they only support PostGreSQL, which I may eventually port it to. Make Crawling Great Again!