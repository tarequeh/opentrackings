from django.conf.urls.defaults import url, patterns, include
from opentrackings.apps.opentrackings import views as opentrackings_views

urlpatterns = patterns('',
    url(r'^$', opentrackings_views.index, name='opentrackings_index'),
    url(r'^shipment/all/$', opentrackings_views.view_shipments, name='opentrackings_view_shipments'),
    url(r'^shipment/add/$', opentrackings_views.add_shipment, name='opentrackings_add_shipment'),
    url(r'^shipment/(?P<shipment_id>\d+)/view/$', opentrackings_views.view_shipment, name='opentrackings_view_shipment'),
    #url(r'^shipment/(?P<shipment_id>\d+)/edit/$', opentrackings_views.edit_shipment, name='opentrackings_edit_shipment'),
)
