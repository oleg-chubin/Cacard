from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    url(r'^$', 'Cacard.calling_card.views.home', name='home'),
    url(r'^about$', 'Cacard.calling_card.views.about', name='about'),
    url(r'^news/$', 'Cacard.calling_card.views.news', name='news'),
    
    # url(r'^Cacard/', include('Cacard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
