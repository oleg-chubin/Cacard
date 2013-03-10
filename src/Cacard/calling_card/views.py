# Create your views here.

from googlemaps import GoogleMaps
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import News, Product, Brand, ConsumerInfo
from models import ConsumerCategory, ProductCategory, Address
from forms import ConsumerFeedback
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter

menu_register = {}


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


def top_level_menu(item, link, order):
    menu_register.setdefault(item, {})
    menu_register[item].update({'link': link, 'order': order})

    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            res['menu_list'] = [{'name': i, 'active': item == i,
                                 'link': menu_register[i]['link'], 'order': menu_register[i]['order']} for i in menu_register]
            res['menu_list'].sort(key=itemgetter('order'))
            return res
        return wrapper
    return decorator


@render_to("about.html")
@top_level_menu("Home", "", 1)
def home(request):
    brands = Brand.objects.all()
    product_categorys = ProductCategory.objects.all()
    return  {'brands': brands, 'product_categorys': product_categorys}


@render_to("about.html")
@top_level_menu("About", "about", 2)
def about(request):
    return {}


@render_to("contacts.html")
@top_level_menu("Contacts", "contacts", 6)
def contacts(request):
    contacts = []
    gmaps = GoogleMaps('')
    for addr in Address.objects.all():
        lat, lng = gmaps.address_to_latlng(addr.address)
        contacts.append({'contact':addr,
                         'longitude': lng,
                         'latitude': lat})

    need_form = True
    if request.method == 'POST':
        form = ConsumerFeedback(request.POST)
        if form.is_valid():
            need_form = False
            form.save()
            return {'contacts': contacts, 'need_form': need_form}
    else:
        form = ConsumerFeedback()
    return {'contacts': contacts,
            'form': form,
            'need_form': need_form}


@render_to("customer.html")
@top_level_menu("Customer", "customer", 5)
def customer(request, select='0'):
    categorys = ConsumerCategory.objects.all()
    context = ''
    if select == '0':
        need_url = True
    else:
        need_url = False
    if select:
        context = ConsumerInfo.objects.filter(consumercategory = select)
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
    return {'context': cont_to_view, 'categorys': categorys,
            'customer_item': int(select), 'need_url': need_url}


@render_to("products.html")
@top_level_menu("Products", "product", 3)
def product(request, brand_id='0', prod='0'):
#    products = Product.objects.all()
    brands = Brand.objects.all()
    need_url = False
    product_categorys = ProductCategory.objects.all()
    if brand_id and prod != '0':
        products = Product.objects.filter(brand = brand_id, productcategory = prod)
    elif brand_id and prod == '0':
        products = Product.objects.filter(brand = brand_id)
    if brand_id == '0':
        need_url = True
    else:
        need_url = False
    return {'prod_item': int(brand_id),'prodcat_item': int(prod), 'products': products,
            'brands': brands, 'product_categorys': product_categorys, 'need_url': need_url}


@render_to("news.html")
@top_level_menu("News", "news", 4)
def news(request):
    news_to_view = News.objects.all()
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
    return {'News': cur_news}


@render_to("admin.html")
@top_level_menu("Admin", "admin", 999)
def admin(request):
    return {}


@render_to("order.html")
@top_level_menu("Contacts", "contacts", 6)
def order(request):
    return {}

