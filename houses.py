# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
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
        self.singleHouse = '67 Lynmouth Dr Ruislip HA4 9BY UK'  # 67 Lynmouth Dr Ruislip HA4 9BY UK

        pass

    def sample_house(self):

        self.house_dict = {self.singleHouse: None}

    def get_houses_os_walk(self):

        houses = [x[0] for x in os.walk(home + '/Dropbox/Lanu/houses/') if '_Lynmouth' in x[0]]
        houses = [os.path.basename(h) for h in houses]
        houses = [h.replace("_", " ") for h in houses]

        self.house_dict = dict.fromkeys(houses, 1)

    def geo_locate_houses(self):

        for address in self.house_dict.keys():

            geolocator = GoogleV3(api_key=constants.GOOGLE_API_KEY)
            location = geolocator.geocode(address)
            # get coord in EPSG:27700
            input = Proj(init='EPSG:4326')
            output = Proj(init='EPSG:4326')
            x, y = transform(input, output, location.longitude, location.latitude)

            input = Proj(init='EPSG:4326')
            output = Proj(init='EPSG:27700')
            x1, y1 = transform(input, output, location.longitude, location.latitude)

            dict = {'x': x, 'y': y, 'x1':x1,'y1': y1, 'location': location}
            # self.house_dict[address]['x'] = x,self.house_dict[address]['y'] = y
            # self.house_dict[address]['x1'] = x1,self.house_dict[address]['y1'] = y1
            self.house_dict[address] = dict
