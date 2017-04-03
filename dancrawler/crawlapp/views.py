from django.shortcuts import render, render_to_response
from crawlapp.models import Trump_Tweets
from crawlapp.models import Trump_Articles
#import subprocess

# Create your views here.
def index(request):
	#Runs python script as a subprocess while django server is running :)
	#if request.method == "POST":
	#	subprocess.call(["python", "dancrawler.py"])
	tweets = Trump_Tweets.objects.all()
	articles = Trump_Articles.objects.all()
	
	return render_to_response('index.html', {'tweets':tweets, 'articles':articles})








