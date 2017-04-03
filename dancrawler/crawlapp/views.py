from django.shortcuts import render, render_to_response
#from django.template.response import TemplateResponse
from crawlapp.models import Trump_Tweets
from crawlapp.models import Trump_Articles
#import subprocess

# Create your views here.
def index(request):
	#Runs python script as a subprocess while django server is running :)
	#if request.method == "POST":
	#	subprocess.call(["python", "dancrawler.py"])

	data = Trump_Tweets.objects.order_by('id')[:]
	
	
	return render_to_response('index.html', {"data":data})








