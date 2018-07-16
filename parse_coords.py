#!/usr/bin/python3

# Extract the latitude and longitude coordinates from a request URL
# captured from Chrome Dev Tool's network tab.

import re

request_url = input('Paste request URL: ')

result = re.match('.*xmin%22%3A(\d+\.?\d*).*ymin%22%3A(\d+\.?\d*).*xmax%22%3A(\d+\.?\d*).*ymax%22%3A(\d+\.?\d*).*', request_url)

xmin = result.group(1)
ymin = result.group(2)
xmax = result.group(3)
ymax = result.group(4)

print("Min: ", ymin + "," + xmin)
print("Max: ", ymax + "," + xmax)
