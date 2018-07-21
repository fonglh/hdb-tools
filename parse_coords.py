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

if __name__ == "__main__":
    request_url = input('Paste request URL: ')
    coordinates = extract_coordinates(request_url)

    print("Min: ", coordinates[0])
    print("Max: ", coordinates[1])
