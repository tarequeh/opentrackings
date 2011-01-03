import urllib2

from shipping.constants import UPS_API_KEY, UPS_USERID, UPS_PASSWORD, UPS_INTEGRATION_URL
from shipping.utils import PrintableElementTree

from xml.etree.ElementTree import Element, ElementTree, SubElement

class UPSConnector(object):
    def build_request(self, tracking_number):
        # Build AccessRequest
        access_request = Element("AccessRequest")
        access_request.set("xml:lang", "en-US")

        license_number = SubElement(access_request, "AccessLicenseNumber")
        license_number.text = UPS_API_KEY

        user_id = SubElement(access_request, "UserId")
        user_id.text = UPS_USERID

        password = SubElement(access_request, "Password")
        password.text = UPS_PASSWORD

        # Build TrackRequest
        track_request = Element("TrackRequest")
        track_request.set("xml:lang", "en-US")

        request_element = SubElement(track_request, "Request")

        transaction_reference = SubElement(request_element, "TransactionReference")

        customer_context = SubElement(transaction_reference, "CustomerContext")
        customer_context.text = "Tracking package %s" % tracking_number
        xpci_version = SubElement(transaction_reference, "XpciVersion")
        xpci_version.text = "1.0"

        request_action = SubElement(request_element, "RequestAction")
        request_action.text = "Track"

        request_option = SubElement(request_element, "RequestOption")
        request_option.text = "1"

        tracking_number_element = SubElement(track_request, "TrackingNumber")
        tracking_number_element.text = tracking_number

        access_request_tree = PrintableElementTree(access_request)
        track_request_tree = PrintableElementTree(track_request)

        request_xml = '<?xml version="1.0"?>' + access_request_tree.print_tree() + '<?xml version="1.0"?>' + track_request_tree.print_tree()

        return request_xml

    def get_tracking_information(self, tracking_number):
        request_xml = self.build_request(tracking_number)

        request = urllib2.Request(url=UPS_INTEGRATION_URL, data=request_xml)
        response = urllib2.urlopen(request)

        result_xml = response.read()
        return result_xml
