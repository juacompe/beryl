from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('beryl.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^accounts/login/', 'mylogin', name='login'),
    url(r'^accounts/logout/', 'mylogout', name='logout'),
    # url(r'^beryl/', include('beryl.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^school/',   include('school.urls')),
    url(r'^finance/',   include('finance.urls')),
)
