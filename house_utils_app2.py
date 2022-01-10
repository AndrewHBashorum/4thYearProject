import re
from geopy.geocoders import GoogleV3
import constants_app2
from pyproj import Proj, transform
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def find_id(address):
    reobj = re.compile(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)')
    matchobj = reobj.search(address)
    if matchobj:
        postcode = matchobj.group(1)
        postcode = postcode.replace(" ", "_")
        address = address.split(' ')
        house_number = address[0]
        id = address[0] + '_' + postcode
        return id, house_number, postcode
    else:
        return None, None, None

def geo_locate_houses_alt(address):

    geolocator = GoogleV3(api_key=constants_app2.GOOGLE_API_KEY)
    location = geolocator.geocode(address)

    # get coord in EPSG:27700
    input = Proj(init='EPSG:4326')
    output = Proj(init='EPSG:4326')
    xd, yd = transform(input, output, location.longitude, location.latitude)

    input = Proj(init='EPSG:4326')
    output = Proj(init='EPSG:27700')
    xt, yt = transform(input, output, location.longitude, location.latitude)

    id_house, house_number, postcode = find_id(address)

    return id_house, house_number, postcode, xt, yt, xd, yd

def point_in_polygon(px, py, x, y):
    # returns True if point (px, py) is in polygon (x, y) and False otherwise
    x0, y0 = x[:], y[:]
    c = False
    n = len(x0)
    for i in range(n):
        j = (i - 1) % len(x0)
        if (((y0[i] > py) != (y0[j] > py)) and (
                px >= ((x0[j] - x0[i]) * (py - y0[i]) / (y0[j] - y0[i])) + x0[i])):
            c = not c
    return c