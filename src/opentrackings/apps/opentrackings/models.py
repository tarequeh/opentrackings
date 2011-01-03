import datetime
from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from opentrackings.apps.base.models import BaseModel
from opentrackings.apps.opentrackings.constants import SHIPMENT_SERVICE_PROVIDER_CHOICES

class Address(BaseModel):
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state_province = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)

class Shipper(BaseModel):
    shipper_number = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address)

    class Meta:
        unique_together = (("shipper_number", "address"),)

class Receiver(BaseModel):
    receiver_number = models.CharField(max_length=50, blank=True)
    address = models.ForeignKey(Address)

    class Meta:
        unique_together = (("receiver_number", "address"),)

class Shipment(BaseModel):
    tracking_number = models.CharField(max_length=100)
    subscriber = models.ForeignKey(User, related_name='shipments')
    provider = models.CharField(max_length=20, choices=SHIPMENT_SERVICE_PROVIDER_CHOICES)
    shipper = models.ForeignKey(Shipper, related_name='shipments', blank=True, null=True)
    receiver = models.ForeignKey(Receiver, related_name='shipments', blank=True, null=True)

    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=2000, blank=True)

    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(max_length=20, blank=True)
    service_code = models.CharField(max_length=20, blank=True)
    service_description = models.CharField(max_length=50, blank=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    scheduled_delivery_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("tracking_number", "subscriber"),)

    def get_shipping_handler(self):
        return get_shipping_handler(self.provider)

class Package(BaseModel):
    tracking_number = models.CharField(max_length=100)
    shipment = models.ForeignKey(Shipment, related_name='packages')
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=2000, blank=True)

    class Meta:
        unique_together = (("tracking_number", "shipment"),)

class Activity(BaseModel):
    package = models.ForeignKey(Package, related_name='activities')
    time = models.DateTimeField()
    address = models.ForeignKey(Address)
    status_code = models.CharField(max_length=20, blank=True)
    status_description = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ('time',)
        get_latest_by = 'time'

admin.site.register(Shipper)
admin.site.register(Receiver)
admin.site.register(Shipment)
admin.site.register(Package)
admin.site.register(Activity)
admin.site.register(Address)
