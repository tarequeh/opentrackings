from django import forms
from django.core.exceptions import ValidationError

from opentrackings.apps.opentrackings.constants import SHIPMENT_SERVICE_PROVIDER_CHOICES
from opentrackings.apps.opentrackings.utils import get_shipment_provider, get_shipment_handler, get_shipment

class ShipmentTrackingForm(forms.Form):
    tracking_number = forms.CharField(label=u'Tracking Number')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ShipmentTrackingForm, self).__init__(*args, **kwargs)

    def clean_tracking_number(self):
        cleaned_data = self.cleaned_data
        tracking_number = cleaned_data.get('tracking_number', '')

        shipment_provider = get_shipment_provider(tracking_number)

        if shipment_provider == None:
            raise ValidationError("Not a valid %s tracking number." % "/".join(dict(SHIPMENT_SERVICE_PROVIDER_CHOICES).values()))

        try:
            shipment_handler = get_shipment_handler(shipment_provider)
        except Exception, e:
            raise ValidationError(str(e))

        shipment = get_shipment(tracking_number, self.user)
        if shipment != None:
            raise ValidationError("Shipment record already exists.")

        return tracking_number

    def save(self):
        cleaned_data = self.cleaned_data
        tracking_number = cleaned_data.get('tracking_number', '')        

        shipment_provider = get_shipment_provider(tracking_number)
        shipment_handler = get_shipment_handler(shipment_provider)

        shipment = shipment_handler.create_shipment(tracking_number, self.user)

        return shipment
