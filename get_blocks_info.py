#!/usr/bin/python3

from get_blocks import *
from get_info import *
import csv

# Test area north of the Geylang River
min_point = [1.30176, 103.88122]
max_point = [1.30725, 103.88671]

all_blocks = get_blocks(min_point, max_point)

with open('block_info.csv', 'w') as csvfile:
    fieldnames = ['address', 'postal_code', 'town_name', 'town_code',
                  'lease_commenced_date', 'lease_remaining', 'lease_period', 'building_gl']
    block_info_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    block_info_writer.writeheader()

    for block in all_blocks:
        lease_info = get_lease_info(block['postal_code'])
        property_info = get_property_info(block['building_gl'])
        block_info = {}
        block_info['address'] = property_info['block'] + ' ' + property_info['street_name']
        block_info['postal_code'] = block['postal_code']
        block_info['town_code'] = property_info['town_code']
        block_info['town_name'] = property_info['town_name']
        block_info['lease_commenced_date'] = lease_info['lease_commenced_date']
        block_info['lease_remaining'] = lease_info['lease_remaining']
        block_info['lease_period'] = lease_info['lease_period']
        block_info['building_gl'] = block['building_gl']
        print(block_info)
        block_info_writer.writerow(block_info)
