#!/usr/bin/python3

import re

# Extract the latitude and longitude coordinates from a request URL
# captured from Chrome Dev Tool's network tab.
def extract_coordinates(request_url):
    result = re.match('.*xmin%22%3A(\d+\.?\d*).*ymin%22%3A(\d+\.?\d*).*xmax%22%3A(\d+\.?\d*).*ymax%22%3A(\d+\.?\d*).*', request_url)
    xmin = float(result.group(1))
    ymin = float(result.group(2))
    xmax = float(result.group(3))
    ymax = float(result.group(4))
    return ((ymin, xmin), (ymax, xmax))

# Given (lat, lng) for min (bottom left) and max (top right) points, generate the URL.
def coords_to_url(min_point, max_point):
    return "https://services2.hdb.gov.sg/ej03map/rest/services/Internal/HDBBuilding/MapServer/0/query?returnGeometry=false&where=&outSr=4326&outFields=*&inSr=4326&geometry=%7B%22xmin%22%3A" + \
        str(min_point[1]) + "%2C%22ymin%22%3A" + str(min_point[0]) + "%2C%22xmax%22%3A" + str(max_point[1]) + "%2C%22ymax%22%3A" + str(max_point[0]) + "%2C%22spatialReference%22%3A%7B%22wkid%22%3A4326%7D%7D&" + \
        "geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&geometryPrecision=6&f=json"

#request_url = input('Paste request URL: ')
#coordinates = extract_coordinates(request_url)

#print("Min: ", coordinates[0])
#print("Max: ", coordinates[1])
