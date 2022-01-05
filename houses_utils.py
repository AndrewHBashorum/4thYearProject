# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
import re
import openpyxl
import os
from pathlib import Path
home = str(Path.home())
if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    import pickle5 as pickle
else:
    user = 'luke'
    import pickle
from geopy.geocoders import GoogleV3
import constants
from pyproj import Proj, transform
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from house import House

def get_houses_os_walk():
    houses = [x[0] for x in os.walk(home + '/Dropbox/Lanu/houses/') if '_Lynmouth' in x[0]]
    houses = [os.path.basename(h) for h in houses]
    houses = [h.replace("_", " ") for h in houses]
    return houses

def spreadsheet_input(sheet_id, excel_file_folder):
    wb = openpyxl.load_workbook(excel_file_folder + 'house_lists.xlsx')
    ws = wb[sheet_id]
    houses = []
    for row in ws['A']:
        houses.append(row.value)
    wb.close()
    return houses

def get_houses_from_pickle():
    with open('site_finder.pickle', 'rb') as f:
        return pickle.load(f)

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

def geo_locate_houses(house_addresses, house_dict):

    for address in house_addresses:
        geolocator = GoogleV3(api_key=constants.GOOGLE_API_KEY)
        location = geolocator.geocode(address)

        # get coord in EPSG:27700
        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:4326')
        xd, yd = transform(input, output, location.longitude, location.latitude)

        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:27700')
        xt, yt = transform(input, output, location.longitude, location.latitude)

        id_house, house_number, postcode = find_id(address)
        house = House()
        house.id = id_house
        house.address = address
        house.postcode = postcode
        house.house_number = int(house_number)
        house.xd = xd
        house.yd = yd
        house.xt = round(xt, 4)
        house.yt = round(yt, 4)
        house.location = location
        house.sites = []
        house.neigh_site = []
        house.potential_neighs = []

        splitAdress = id_house.split('_')
        num = int(splitAdress[0])

        house.potential_neighs.append(num + 2)
        house.potential_neighs.append(num + 4)
        house.potential_neighs.append(num + 6)
        house.potential_neighs.append(num - 2)
        house.potential_neighs.append(num - 4)
        house.potential_neighs.append(num - 6)
        house.potential_neighs = [x for x in house.potential_neighs if x >= 0]

        # house.potential_neighs.append(str(int(num + 2)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
        # house.potential_neighs.append(str(int(num + 4)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
        # house.potential_neighs.append(str(int(num - 2)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
        # house.potential_neighs.append(str(int(num - 4)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))

        house_dict[id_house] = house
    return house_dict


def geo_locate_houses_alt(address):

    geolocator = GoogleV3(api_key=constants.GOOGLE_API_KEY)
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
