# Create your views here.
from django.shortcuts import render_to_response
from Cacard.calling_card.models import News

def home(request):
    return render_to_response("about.html", {})

def news(request):
   
    return render_to_response("news.html", {'News':News.objects.all()})
