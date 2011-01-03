from django.conf.urls.defaults import patterns, url, include, handler500, handler404

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('opentrackings.apps.opentrackings.urls')),
    url(r'^account/', include('django_authopenid.urls')),
)

# Admin URLs
urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
