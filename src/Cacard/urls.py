from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('calling_card.views',

    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about', name='about'),
    url(r'^product/$', 'product', name='product'),
    url(r'^product/(?P<page>\d)/$', 'product', name='product'),
    url(r'^contacts/$', 'contacts', name='contacts'),
    url(r'^customer/$', 'customer', name='customer'),
    url(r'^news/$', 'news', name='news'),
    
    # url(r'^Cacard/', include('Cacard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
