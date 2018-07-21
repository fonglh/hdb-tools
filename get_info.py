#!/usr/bin/python3

# Given a postal code, get the lease info

import time
import urllib.request
import xml.etree.ElementTree as ET

def get_lease_info(postal_code):
    request_url = "https://services2.hdb.gov.sg/webapp/BB14ALeaseInfo/BB14SGenerateLeaseInfoXML?postalCode=" + str(postal_code) + "&_=" + str(int(time.time() * 1000))
    with urllib.request.urlopen(request_url) as url:
        response = url.read().decode()
        root = ET.fromstring(response)
        if root.find('ErrorCode').text == '0000':
            return {
                       'postal_code': postal_code,
                       'lease_commenced_date': root.find('LeaseCommencedDate').text,
                       'lease_remaining': int(root.find('LeaseRemaining').text),
                       'lease_period': int(root.find('LeasePeriod').text)
                   }
        else:
            return { 'postal_code': postal_code, 'lease_commenced_date': None, 'lease_remaining': None, 'lease_period': None }

# Only useful with the get_blocks script as that returns the postal code with the Building GL.
def get_property_info(building_gl):
    request_url = "https://services2.hdb.gov.sg/webapp/BC16AWPropInfoXML/BC16SRetrievePropInfoXML?sysId=FI10&bldngGL=" + str(building_gl)
    with urllib.request.urlopen(request_url) as url:
        response = url.read().decode()
        root = ET.fromstring(response)
        if root.find('ErrorCode').text == '0000':
            return {
                       'building_gl': building_gl,
                       'block': root.find('Block').text.strip(),
                       'street_name': root.find('StreetName').text.strip(),
                       'postal_code': root.find('PostalCode').text.strip(),
                       'town_code': root.find('TownCode').text.strip(),
                       'town_name': root.find('TownName').text.strip(),
                   }
        else:
            return { 'building_gl': building_gl, 'block': None, 'street_name': None, 'postal_code': None, 'town_code': None, 'town_name': None }
        
if __name__ == "__main__":
    postal_code = input("Enter postal code: ")
    info = get_lease_info(postal_code)
    print("Postal Code:", postal_code)
    print("Lease Commenced Date:", info['lease_commenced_date'])
    print("Lease Remaining:", info['lease_remaining'])
    print("Lease Period:", info['lease_period'])
