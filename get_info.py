#!/usr/bin/python3

# Given a postal code, get the lease info

import time
import urllib.request
import xml.etree.ElementTree as ET
# Run `pip3 install tenacity` to install https://github.com/jd/tenacity
from tenacity import *

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def get_lease_info(postal_code):
    time.sleep(0.3)
    request_url = "https://services2.hdb.gov.sg/webapp/BB14ALeaseInfo/BB14SGenerateLeaseInfoXML?postalCode=" + str(postal_code) + "&_=" + str(int(time.time() * 1000))
    req = urllib.request.Request(request_url)
    req.add_header('Referer', 'https://services2.hdb.gov.sg/web/fi10/emap.html')
    with urllib.request.urlopen(req) as url:
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
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def get_property_info(building_gl):
    time.sleep(0.3)
    request_url = "https://services2.hdb.gov.sg/webapp/BC16AWPropInfoXML/BC16SRetrievePropInfoXML?sysId=FI10&bldngGL=" + str(building_gl)
    req = urllib.request.Request(request_url)
    req.add_header('Referer', 'https://services2.hdb.gov.sg/web/fi10/emap.html')
    with urllib.request.urlopen(req) as url:
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

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def get_resale_transactions(postal_code):
    time.sleep(0.3)
    request_url = "https://services2.hdb.gov.sg/webapp/BB33RTISMAP/BB33SResaleTransMap?postal=" + str(postal_code) + "&_=" + str(int(time.time() * 1000))
    req = urllib.request.Request(request_url)
    req.add_header('Referer', 'https://services2.hdb.gov.sg/web/fi10/emap.html')
    transactions = []
    fields = ['postal_code', 'flat_type', 'registration_date', 'block_number', 'floor_range', 'resale_price', 'floor_area', 'lease_commencement_date', 'remaining_lease', 'model']
    with urllib.request.urlopen(req) as url:
        response = url.read().decode()
        root = ET.fromstring(response)
        if root.find('errorCode').text == '0000':
            for dataset in root.findall('Dataset'):
                transaction = {}
                for i in range(len(fields)):
                    transaction[fields[i]] = dataset[i].text
                transactions.append(transaction)
    return transactions
        
if __name__ == "__main__":
    postal_code = input("Enter postal code: ")
    info = get_lease_info(postal_code)
    resale_transactions = get_resale_transactions(postal_code)
    print("Postal Code:", postal_code)
    print("Lease Commenced Date:", info['lease_commenced_date'])
    print("Lease Remaining:", info['lease_remaining'])
    print("Lease Period:", info['lease_period'])
    print()
    print("Resale transactions:")
    for sale in resale_transactions:
        print("Flat type: " + sale['flat_type'])
        print("Flat model: " + sale['model'])
        print("Storey: " + sale['floor_range'])
        print("Floor area: " + sale['floor_area'])
        print("Resale price: " + sale['resale_price'])
        print("Resale date: " + sale['registration_date'])
        print()
