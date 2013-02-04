# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import News, Product, Brand, Adress, ConsumerInfo,ConsumerCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

menu_register = set()
def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer

def top_level_menu(item,order):
    menu_register.add(item)
    def decorator(func):
        def wrapper(*args, **kwargs): 
            res = func(*args, **kwargs)
            res['x'] = [{'name':i, 'active': item==i} for i in menu_register]
            return res
        return wrapper
    return decorator

@render_to("about.html")
@top_level_menu("HOME",1)
def home(request):
    return  {'menu_item': "HOME"}


@render_to("about.html")
@top_level_menu("ABOUT",2)
def about(request):
    return {'menu_item': "ABOUT"}

@render_to("contacts.html")
@top_level_menu("CONTACTS",6)
def contacts(request):
    contacts=Adress.objects.all()
    return {'menu_item': "CONTACTS",'contacts':contacts}

@render_to("customer.html")
@top_level_menu("CUSOMER",5)
def customer(request):
    categorys=ConsumerCategory.objects.all()
    context=ConsumerInfo.objects.filter(consumercategory=categorys[0])
    select = request.GET.get('select')
    if select:
        context = ConsumerInfo.objects.filter(consumercategory=select)
    else: 
        select=categorys[0].id

    paginator = Paginator(context, 2) 
    page = request.GET.get('page')
    try:
        cont_to_view = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cont_to_view = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cont_to_view = paginator.page(paginator.num_pages)

    return {'menu_item': "CUSOMER",'context':cont_to_view,
                              'categorys':categorys,'prod_item': int(select)}


@render_to("products.html")
@top_level_menu("PRODUCTS",3)
def product(request):
    products=Product.objects.all()
    brands=Brand.objects.all()
    page = request.GET.get('page')
    if page:
        products = Product.objects.filter(brand=page)
    else: 
        page=0    
    
    return {'menu_item': "PRODUCTS",
                            'prod_item': int(page),'products': products,'brands':brands}


@render_to("news.html")
@top_level_menu("NEWS",4)
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

    return {'menu_item': "NEWS",'News':cur_news}
