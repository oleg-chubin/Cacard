from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('calling_card.views',

    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^about/$', 'about', name='about'),
    url(r'^product/$', 'product', name='product'),
    url(r'^product/(?P<page>\d{1,4})/(?P<prod>\d{1,4})/$', 'product', name='paged_product'),
    url(r'^contacts/$', 'contacts', name='contacts'),
    url(r'^customer/$', 'customer', name='customer'),
    url(r'^customer/(?P<select>\d{1,4})/$', 'customer', name='paged_customer'),
    url(r'^news/$', 'news', name='news'),

    # url(r'^Cacard/', include('Cacard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
