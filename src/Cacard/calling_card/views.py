# Create your views here.
from django.shortcuts import render_to_response
from Cacard.calling_card.models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render_to_response("about.html", {})

def about(request):
    return render_to_response("about.html", {})


def news(request):
    news_to_view=News.objects.all()
    paginator = Paginator(news_to_view, 2) 
    page = request.GET.get('page')
    try:
        cur_news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cur_news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cur_news = paginator.page(paginator.num_pages)

    return render_to_response("news.html", {'News':cur_news})