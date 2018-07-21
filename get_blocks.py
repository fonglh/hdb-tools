#!/usr/bin/python3

# Prompt for min and max point and return all the blocks in the area.

import urllib.request, json, statistics
import time
from coords_to_url import *

# Make the request to HDB's map server then parse the response.
# Extract {lat, lng, OBJECTID, BuildingGL, PostalCode} from each entry.
# Return a list.
def get_blocks(min_point, max_point):
    time.sleep(1)
    request_url = coords_to_url(min_point, max_point)
    with urllib.request.urlopen(request_url) as url:
        blocks = json.loads(url.read().decode())
        if 'exceededTransferLimit' in blocks:
            quadrants = split_quadrants(min_point, max_point)
            all_blocks = []
            for quadrant in quadrants:
                print(quadrant)
                all_blocks += get_blocks(quadrant[0], quadrant[1])
            return all_blocks
        else:
            return list(map(lambda x: {'lat': x['geometry']['y'], 'lng': x['geometry']['x'], 'object_id': x['attributes']['OBJECTID'], 'postal_code': x['attributes']['PostalCode'], 'building_gl': x['attributes']['BuildingGL']}, blocks['features']))

# Given a rectangle bounded by min_point (bottom left) and max_point (top right),
# return a list of coordinates for 4 equally divided quadrants.
#
#                                   x                       max_point
#
#                 1                                 2
#
#     x                          mid_point                     x
#
#                 3                                 4
#
#  min_point                        x
#
def split_quadrants(min_point, max_point):
    mid_point = list(map(lambda x: statistics.mean(x), zip(min_point, max_point)))

    quadrants = []
    quadrants.append([[mid_point[0], min_point[1]], [max_point[0], mid_point[1]]])     # top left rectangle
    quadrants.append([mid_point, max_point])                                           # top right rectangle
    quadrants.append([min_point, mid_point])                                           # bottom left rectangle
    quadrants.append([[min_point[0], mid_point[1]], [mid_point[0], max_point[1]]])     # bottom right rectangle

    return quadrants

if __name__ == "__main__":
    min_point = input("Enter min point (lat,lng): ")
    min_point = min_point.split(',')
    max_point = input("Enter max point (lat,lng): ")
    max_point = max_point.split(',')

    blocks = get_blocks(min_point, max_point)
    print(blocks)
    print(len(blocks))
