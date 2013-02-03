# Create your views here.
from django.shortcuts import render_to_response
from models import News, Product, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def home(request):
    return render_to_response("about.html", {'menu_item': "HOME"})


def about(request):
    return render_to_response("about.html", {'menu_item': "ABOUT"})

def product(request):
    products=Product.objects.all()
    brands=Brand.objects.all()
    
    page = request.GET.get('page')
    if page:
         products = Product.objects.filter(brand=page)
    else: 
        page=0    
    
    return render_to_response("products.html", {'menu_item': "PRODUCTS",
                            'prod_item': int(page),'products': products,'brands':brands})



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

    return render_to_response("news.html", {'menu_item': "NEWS",'News':cur_news})
