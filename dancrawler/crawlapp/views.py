from django.shortcuts import render, render_to_response
from crawlapp.models import Trump_Tweets
from crawlapp.models import Trump_Articles
import subprocess

# Create your views here.
def index(request):
	#Runs python script as a subprocess while django server is running :)
	#When you refresh the website it should run the python script. Approx time 3-4 secs
	subprocess.call(["python", "dancrawler.py"])
	tweets = Trump_Tweets.objects.all()
	#Gets the first 25 Trump articles by the order of id from db
	articles = Trump_Articles.objects.order_by("id")[:25]
    
	return render_to_response('index.html', {'tweets':tweets, 'articles':articles})








