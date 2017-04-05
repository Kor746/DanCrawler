# DanCrawler is an awesome webcrawler that collects the newest Trump tweets and articles. I created this using Python 3.4.1, Django web framework and sqlite3 db. I learned Django while doing this project. The only way to learn! 

!!!MAKE SURE YOU HAVE DJANGO INSTALLED!!!
!!!MAKE SURE YOU PIP INSTALL ALL EXTERNAL MODULES!!!

**RobotParser can be found in this link https://github.com/python-git/python/blob/master/Lib/robotparser.py

=================================================================================
####OUTDATED####

1. Run 'pip install django' in command shell

2. Run 'python dancrawler.py'. This script will crawl the weblinks for data on Trumpity Trump and update the sqlite3 database.

3. Run 'python manage.py runserver' in the same directory. This should start your server and you can access via localhost:8000 on your browser. Enjoy!

=================================================================================

####UPDATES####

I have implemented 'python dancrawler.py' as a subprocess on view.py.

1. Run 'python manage.py runserver'

2. Just refresh the page if you want to update the news/tweets. It should take approx 3-4 seconds.

####Afterthoughts####:

Hopefully, I can find the time to make the UI prettier, deploy it on a hosted server. I tried using heroku's free service, but they only support PostGreSQL, which I may eventually port it to. Make Crawling Great Again!