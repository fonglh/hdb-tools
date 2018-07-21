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
        if root.find('ErrorCode').text == 'NFND':
            return { 'postal_code': postal_code, 'lease_commenced_date': None, 'lease_remaining': None, 'lease_period': None }
        else:
            return {
                       'postal_code': postal_code,
                       'lease_commenced_date': root.find('LeaseCommencedDate').text,
                       'lease_remaining': int(root.find('LeaseRemaining').text),
                       'lease_period': int(root.find('LeasePeriod').text)
                   }
        
if __name__ == "__main__":
    postal_code = input("Enter postal code: ")
    info = get_lease_info(postal_code)
    print("Postal Code:", postal_code)
    print("Lease Commenced Date:", info['lease_commenced_date'])
    print("Lease Remaining:", info['lease_remaining'])
    print("Lease Period:", info['lease_period'])
