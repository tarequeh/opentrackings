import datetime
import hashlib

from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from opentrackings.apps.opentrackings.forms import ShipmentTrackingForm 
from opentrackings.apps.opentrackings.models import Shipment

@login_required
def index(request):
    return HttpResponseRedirect(reverse('opentrackings_view_shipments'))

@login_required
def view_shipments(request):
    shipments = request.user.shipments.all()

    return render_to_response('opentrackings/view_shipments.html', {
        'shipments': shipments,
    }, context_instance=RequestContext(request))

@login_required
def view_shipment(request, shipment_id):
    try:
        shipment = Shipment.objects.get(pk=shipment_id)
    except Shipment.DoesNotExist:
        raise Http404

    return render_to_response('opentrackings/view_shipment.html', {
        'shipment': shipment,
    }, context_instance=RequestContext(request))

@login_required
def add_shipment(request):
    if request.method == 'POST':
        form = ShipmentTrackingForm(data=request.POST, user=request.user)
        if form.is_valid():
            shipment = form.save()
            return HttpResponseRedirect(reverse('opentrackings_view_shipment', args=[shipment.pk]))
    else:
        form = ShipmentTrackingForm()
    
    return render_to_response('opentrackings/add_shipment.html', {
        'form': form,
    }, context_instance=RequestContext(request))
