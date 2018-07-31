#!/usr/bin/python3

from get_blocks import *
from get_info import *
import csv
import psycopg2
import os

# Assume database named hdb is already created and use peer authentication with the current user.
conn = psycopg2.connect("dbname=hdb user=" + os.getlogin())
cursor = conn.cursor()
blocks_sql = "INSERT INTO blocks(postal_code, address, town_name, town_code, lease_commenced_date, lease_remaining, lease_period, building_gl) " \
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (postal_code) DO NOTHING"

#min_point = [1.31013, 103.86564]
#max_point = [1.33566, 103.89676]
min_point = [1.31171, 103.87205]
max_point = [1.31557, 103.87350]

all_blocks = get_blocks(min_point, max_point)

all_blocks_info = []
all_resale_transactions = []

for block in all_blocks:
    lease_info = get_lease_info(block['postal_code'])
    resale_transactions = get_resale_transactions(block['postal_code'])
    for transaction in resale_transactions:
        all_resale_transactions.append(transaction)
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
    all_blocks_info.append(block_info)

with open('block_info.csv', 'w') as csvfile:
    fieldnames = ['address', 'postal_code', 'town_name', 'town_code',
                  'lease_commenced_date', 'lease_remaining', 'lease_period', 'building_gl']
    block_info_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    block_info_writer.writeheader()
    for block_info in all_blocks_info:
        block_info_writer.writerow(block_info)
        cursor.execute(blocks_sql, (block_info['postal_code'], block_info['address'], block_info['town_name'], block_info['town_code'],
                                    block_info['lease_commenced_date'], block_info['lease_remaining'], block_info['lease_period'], block_info['building_gl']))
    conn.commit()
cursor.close()
conn.close()

with open('resale_transactions.csv', 'w') as csvfile:
    fieldnames = ['postal_code', 'flat_type', 'registration_date', 'block_number', 'floor_range', 'resale_price', 'floor_area', 'lease_commencement_date', 'remaining_lease', 'model']
    resale_transactions_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    resale_transactions_writer.writeheader()
    for transaction in all_resale_transactions:
        print(transaction)
        resale_transactions_writer.writerow(transaction)
