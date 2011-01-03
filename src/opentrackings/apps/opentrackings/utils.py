import datetime
import re

from django.db import transaction

from opentrackings.apps.opentrackings.constants import SHIPMENT_SERVICE_PROVIDER_UPS
from opentrackings.apps.opentrackings.constants import TRACKING_NUMBER_PATTERN_UPS, TRACKING_NUMBER_PATTERN_FEDEX, TRACKING_NUMBER_PATTERN_DHL, TRACKING_NUMBER_PATTERN_USPS
from opentrackings.apps.opentrackings.models import Shipment, Shipper, Receiver, Activity, Package, Address

from shipping.connectors import UPSConnector
from shipping.utils import PrintableElementTree, get_element_text

class ShippingHandler(object):
    def create_shipment(self, tracking_number, subscriber):
        pass 

    def update_shipment(self, shipment):
        pass    

class UPSHandler(ShippingHandler):
    @transaction.commit_on_success
    def create_shipment(self, tracking_number, subscriber):
        ups_connector = UPSConnector()
        tracking_response = ups_connector.get_tracking_information(tracking_number)
        #tracking_response = '<?xml version="1.0"?>\n<TrackResponse><Response><TransactionReference><CustomerContext>Tracking package 1Z8Y875V0310424142</CustomerContext><XpciVersion>1.0</XpciVersion></TransactionReference><ResponseStatusCode>1</ResponseStatusCode><ResponseStatusDescription>Success</ResponseStatusDescription></Response><Shipment><Shipper><ShipperNumber>8Y875V</ShipperNumber><Address><AddressLine1>1100 WESTLAKE PKWY SW</AddressLine1><AddressLine2>SUITE 120</AddressLine2><City>ATLANTA</City><StateProvinceCode>GA</StateProvinceCode><PostalCode>30336   2937</PostalCode><CountryCode>US</CountryCode></Address></Shipper><ShipTo><Address><City>ARLINGTON</City><StateProvinceCode>VA</StateProvinceCode><PostalCode>22202</PostalCode><CountryCode>US</CountryCode></Address></ShipTo><ShipmentWeight><UnitOfMeasurement><Code>LBS</Code></UnitOfMeasurement><Weight>7.00</Weight></ShipmentWeight><Service><Code>003</Code><Description>GROUND</Description></Service><ShipmentIdentificationNumber>1Z8Y875V0310424142</ShipmentIdentificationNumber><PickupDate>20100826</PickupDate><ScheduledDeliveryDate>20100830</ScheduledDeliveryDate><Package><TrackingNumber>1Z8Y875V0310424142</TrackingNumber><Activity><ActivityLocation><Address><City>ALEXANDRIA</City><StateProvinceCode>VA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>IN TRANSIT TO</Description></StatusType><StatusCode><Code>IT</Code></StatusCode></Status><Date>20100828</Date><Time>025200</Time></Activity><Activity><ActivityLocation><Address><City>RICHMOND</City><StateProvinceCode>VA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>DEPARTURE SCAN</Description></StatusType><StatusCode><Code>DP</Code></StatusCode></Status><Date>20100828</Date><Time>025100</Time></Activity><Activity><ActivityLocation><Address><City>RICHMOND</City><StateProvinceCode>VA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>LOCATION SCAN</Description></StatusType><StatusCode><Code>LC</Code></StatusCode></Status><Date>20100827</Date><Time>192700</Time></Activity><Activity><ActivityLocation><Address><City>RICHMOND</City><StateProvinceCode>VA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>ARRIVAL SCAN</Description></StatusType><StatusCode><Code>AR</Code></StatusCode></Status><Date>20100827</Date><Time>134200</Time></Activity><Activity><ActivityLocation><Address><City>DORAVILLE</City><StateProvinceCode>GA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>DEPARTURE SCAN</Description></StatusType><StatusCode><Code>DP</Code></StatusCode></Status><Date>20100827</Date><Time>032000</Time></Activity><Activity><ActivityLocation><Address><City>DORAVILLE</City><StateProvinceCode>GA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>ARRIVAL SCAN</Description></StatusType><StatusCode><Code>AR</Code></StatusCode></Status><Date>20100827</Date><Time>013000</Time></Activity><Activity><ActivityLocation><Address><City>ATLANTA</City><StateProvinceCode>GA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>DEPARTURE SCAN</Description></StatusType><StatusCode><Code>DP</Code></StatusCode></Status><Date>20100827</Date><Time>005100</Time></Activity><Activity><ActivityLocation><Address><City>ATLANTA</City><StateProvinceCode>GA</StateProvinceCode><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>I</Code><Description>ORIGIN SCAN</Description></StatusType><StatusCode><Code>OR</Code></StatusCode></Status><Date>20100826</Date><Time>192200</Time></Activity><Activity><ActivityLocation><Address><CountryCode>US</CountryCode></Address></ActivityLocation><Status><StatusType><Code>M</Code><Description>BILLING INFORMATION RECEIVED</Description></StatusType><StatusCode><Code>MP</Code></StatusCode></Status><Date>20100826</Date><Time>172438</Time></Activity><Message><Code>01</Code><Description>On Time</Description></Message><PackageWeight><UnitOfMeasurement><Code>LBS</Code></UnitOfMeasurement><Weight>7.00</Weight></PackageWeight><ReferenceNumber><Code>01</Code><Value>P594078</Value></ReferenceNumber><ReferenceNumber><Code>01</Code><Value>00000000000092287872</Value></ReferenceNumber><ReferenceNumber><Code>01</Code><Value>82621</Value></ReferenceNumber></Package></Shipment></TrackResponse>'

        tracking_parser = PrintableElementTree()
        tracking_parser.parse_xml(tracking_response)

        error_element = tracking_parser.find("//Error")

        if error_element != None:
            error_code = get_element_text(tracking_parser.find("//ErrorCode"), "N/A")
            error_description = get_element_text(tracking_parser.find("//ErrorDescription"), "N/A")

            raise Exception("Error creating shipment. Error Code: %s Description: %s" % (error_code, error_description))
        else:
            shipment_element = tracking_parser.find("//Shipment")
            if shipment_element == None:
                raise Exception("Could not locate shipment information.")

            shipment = Shipment()
            shipment.subscriber = subscriber
            shipment.tracking_number = shipment_element.find("ShipmentIdentificationNumber").text
            shipment.provider = SHIPMENT_SERVICE_PROVIDER_UPS

            shipment.save()

            shipper_element = shipment_element.find("Shipper")
            if shipper_element != None:
                shipper = Shipper()
                shipper.shipper_number = get_element_text(shipper_element.find("ShipperNumber"))
                if shipper_element.find("Address") != None:
                    address = Address()
                    address.address_line_1 = get_element_text(shipper_element.find("Address/AddressLine1"))
                    address.address_line_2 = get_element_text(shipper_element.find("Address/AddressLine2"))
                    address.city = get_element_text(shipper_element.find("Address/City"))
                    address.state_province = get_element_text(shipper_element.find("Address/StateProvinceCode"))
                    address.zipcode = re.sub("\s+", "-", get_element_text(shipper_element.find("Address/PostalCode")))
                    address.country = get_element_text(shipper_element.find("Address/CountryCode"))
                    address.save()
                    shipper.address = address

                shipper.save()
                shipment.shipper = shipper

            receiver_element = shipment_element.find("ShipTo")
            if receiver_element != None:
                receiver = Receiver()

                address = Address()
                address.address_line_1 = get_element_text(receiver_element.find("Address/AddressLine1"))
                address.address_line_2 = get_element_text(receiver_element.find("Address/AddressLine2"))
                address.city = get_element_text(receiver_element.find("Address/City"))
                address.state_province = get_element_text(receiver_element.find("Address/StateProvinceCode"))
                address.zipcode = re.sub("\s+", "-", get_element_text(receiver_element.find("Address/PostalCode")))
                address.country = get_element_text(receiver_element.find("Address/CountryCode"))
                address.save()

                receiver.address = address
                receiver.save()
                shipment.receiver = receiver

            shipment_weight_element = shipment_element.find("ShipmentWeight")
            if shipment_weight_element != None:
                shipment.weight = get_element_text(shipment_weight_element.find("Weight"))
                shipment.weight_unit = get_element_text(shipment_weight_element.find("UnitOfMeasurement/Code"))

            service_element = shipment_element.find("Service")
            if service_element != None:
                shipment.service_code = get_element_text(service_element.find("Code"))
                shipment.service_description = get_element_text(service_element.find("Description"))

            pickup_date_element = shipment_element.find("PickupDate")
            if pickup_date_element != None:
                shipment.pickup_date = datetime.datetime.strptime(pickup_date_element.text, "%Y%m%d")

            scheduled_delivery_date_element = shipment_element.find("ScheduledDeliveryDate")
            if scheduled_delivery_date_element != None:
                shipment.scheduled_delivery_date = datetime.datetime.strptime(scheduled_delivery_date_element.text, "%Y%m%d")

            shipment.save()

            package_elements = shipment_element.findall("Package")
            for package_element in package_elements:
                package = Package()
                package.shipment = shipment
                package.tracking_number = package_element.find("TrackingNumber").text
                package.save()

                activity_elements = package_element.findall("Activity")
                for activity_element in activity_elements:
                    activity = Activity()
                    activity.package = package

                    address_element = activity_element.find("ActivityLocation")

                    address = Address()
                    address.address_line_1 = get_element_text(address_element.find("Address/AddressLine1"))
                    address.address_line_2 = get_element_text(address_element.find("Address/AddressLine2"))
                    address.city = get_element_text(address_element.find("Address/City"))
                    address.state_province = get_element_text(address_element.find("Address/StateProvinceCode"))
                    address.zipcode = re.sub("\s+", "-", get_element_text(address_element.find("Address/PostalCode")))
                    address.country = get_element_text(address_element.find("Address/CountryCode"))
                    address.save()        

                    activity.address = address

                    date_element = activity_element.find("Date")
                    time_element = activity_element.find("Time")

                    time_string = date_element.text
                    time_parser = "%Y%m%d" 

                    if time_element != None:
                        time_string = "%s%s" % (time_string, time_element.text)
                        time_parser = "%s%s" % (time_parser, "%H%M%S")

                    activity.time = datetime.datetime.strptime(time_string, time_parser)

                    status_element = activity_element.find("Status")
                    if status_element != None:
                        activity.status_code = get_element_text(status_element.find("StatusCode/Code"))
                        activity.status_description = get_element_text(status_element.find("StatusType/Description"))

                    activity.save()

            return shipment

class ShippingHandlerNotFound(Exception):
    pass

class ShippingHandlerNotSupported(Exception):
    pass

def get_shipment_provider(tracking_number):
    if re.match(TRACKING_NUMBER_PATTERN_UPS, tracking_number):
        return SHIPMENT_SERVICE_PROVIDER_UPS
    elif re.match(TRACKING_NUMBER_PATTERN_FEDEX, tracking_number):
        return SHIPMENT_SERVICE_PROVIDER_FEDEX
    elif re.match(TRACKING_NUMBER_PATTERN_DHL, tracking_number):
        return SHIPMENT_SERVICE_PROVIDER_DHL
    elif re.match(TRACKING_NUMBER_PATTERN_USPS, tracking_number):
        return SHIPMENT_SERVICE_PROVIDER_USPS
    else:
        return None

def get_shipment_handler(provider):
    provider_handler = None
    if provider == SHIPMENT_SERVICE_PROVIDER_UPS:
        provider_handler = UPSHandler()
    elif provider == SHIPMENT_SERVICE_PROVIDER_FEDEX:
        raise ShippingHandlerNotSupported("FedEx tracking not supported yet.")
    elif provider == SHIPMENT_SERVICE_PROVIDER_DHL:
        raise ShippingHandlerNotSupported("DHL tracking not supported yet.")
    elif provider == SHIPMENT_SERVICE_PROVIDER_USPS:
        raise ShippingHandlerNotSupported("USPS tracking not supported yet.")
    else:
        raise ShippingHandlerNotFound("Tracking number could not be traced to a shipper.")

    return provider_handler

def get_shipment(tracking_number, subscriber):
    try:
        shipment = Shipment.objects.get(tracking_number=tracking_number, subscriber=subscriber)
        return shipment
    except Shipment.DoesNotExist:
        try:
            packages = Package.objects.get(tracking_number=tracking_number, shipment__subscriber=subscriber)
            return package.shipment
        except Package.DoesNotExist:
            return None
