# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
import re

import numpy as np
import json
import pickle5 as pickle
import os
from os import path
from pathlib import Path
import matplotlib.pyplot as plt
import sys
import psycopg2
home = str(Path.home())
from geopy.geocoders import GoogleV3
import constants
from pyproj import Proj, transform
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
class Houses(object):
    def __init__(self):

        self.house_dict = {}
        self.singleHouse = ['67 Lynmouth Dr Ruislip HA4 9BY UK', '35 Lynmouth Dr Ruislip HA4 9BY UK']  # 67 Lynmouth Dr Ruislip HA4 9BY UK

        pass

    def sample_house(self):

        self.houses_address = self.singleHouse
        #self.house_dict = {self.singleHouse: None}

    def get_houses_os_walk(self):

        houses = [x[0] for x in os.walk(home + '/Dropbox/Lanu/houses/') if '_Lynmouth' in x[0]]
        houses = [os.path.basename(h) for h in houses]
        houses = [h.replace("_", " ") for h in houses]
        self.houses_address = houses
        self.house_dict = {}

    def find_id(self, address):

        print(address)

        reobj = re.compile(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)')
        matchobj = reobj.search(address)
        if matchobj:
            self.postcode = matchobj.group(1)
            self.postcode = self.postcode.replace(" ", "_")
            #postcode = postcode.replace("", "_")
        else:
            self.postcode = '____'


        address = address.split(' ')
        self.house_number = address[0]
        id = address[0] + '_' + self.postcode
        return id

    def geo_locate_houses(self):

        for address in self.houses_address:
            print(address)
            geolocator = GoogleV3(api_key=constants.GOOGLE_API_KEY)
            location = geolocator.geocode(address)
            # get coord in EPSG:27700
            input = Proj(init='EPSG:4326')
            output = Proj(init='EPSG:4326')
            x, y = transform(input, output, location.longitude, location.latitude)

            input = Proj(init='EPSG:4326')
            output = Proj(init='EPSG:27700')
            x1, y1 = transform(input, output, location.longitude, location.latitude)

            id_house = self.find_id(address)
            dict = {'id':id_house,'address':address,'postcode': self.postcode,'house_number': self.house_number,'Point_original_x': x, 'Point_original_y': y, 'Point_converted_x':x1,'Point_converted_y': y1, 'location': location, 'sites': [], 'neigh_site': [],'potential_neighs': []}

            splitAdress = id_house.split('_')
            print(splitAdress[0])
            num = int(splitAdress[0])

            dict['potential_neighs'].append(str(int(num + 2)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
            dict['potential_neighs'].append(str(int(num + 4)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
            dict['potential_neighs'].append(str(int(num - 2)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))
            dict['potential_neighs'].append(str(int(num - 4)) + '_' + str(splitAdress[1]) + '_' + str(splitAdress[2]))



            # self.house_dict[address]['x'] = x,self.house_dict[address]['y'] = y
            # self.house_dict[address]['x1'] = x1,self.house_dict[address]['y1'] = y1
            self.house_dict[id_house] = dict
