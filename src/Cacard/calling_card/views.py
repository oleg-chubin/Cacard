# Create your views here.
from django.shortcuts import render_to_response
from Cacard.calling_card.models import News


def home(request):
    return render_to_response("about.html", {'menu_item': "HOME"})


def about(request):
    return render_to_response("about.html", {'menu_item': "ABOUT"})


def news(request):
    context = {'News':News.objects.all(),
               'menu_item': "NEWS"}
    return render_to_response("news.html", context)
