#!/usr/bin/python3

# Given (lat, lng) for min (bottom left) and max (top right) points, generate the URL.
def coords_to_url(min_point, max_point):
    return "https://services2.hdb.gov.sg/ej03map/rest/services/Internal/HDBBuilding/MapServer/0/query?returnGeometry=true&where=&outSr=4326&outFields=*&inSr=4326&geometry=%7B%22xmin%22%3A" + \
        str(min_point[1]) + "%2C%22ymin%22%3A" + str(min_point[0]) + "%2C%22xmax%22%3A" + str(max_point[1]) + "%2C%22ymax%22%3A" + str(max_point[0]) + "%2C%22spatialReference%22%3A%7B%22wkid%22%3A4326%7D%7D&" + \
        "geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&geometryPrecision=6&f=json"

if __name__ == "__main__":
    min_point = input('Enter min point coords (lat,lng): ')
    min_point = min_point.split(',')
    max_point = input('Enter max point coords (lat,lng): ')
    max_point = max_point.split(',')

    print(coords_to_url(min_point, max_point))
