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
from database_interaction import Database
from geometry import Geometry
from pyproj import Proj, transform

sys.path.append(path.abspath(str(Path.home())))
sys.path.append(path.abspath(str(Path.home()) + '/4thYearProject'))
if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
else:
    user = 'luke'
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path
import psycopg2

class Sites(object):
    def __init__(self):

        self.id = 0
        self.gt = Geometry()
        if user == 'andrew':
            self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD", host="localhost",
                                   port="5432")
        else:
            self.con = psycopg2.connect(database="nps_database_cropped", user="postgres", password="$£x25zeD",
                                        host="localhost", port="5433")
        self.cur = self.con.cursor()
        self.GIS = Database()
        self.dict = {}
        pass

    def take_from_database(self, x, y, x1, y1, address):

        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.address = address

        self.geometry = self.GIS.ST_Contains(x,y)
        self.geomForDict = self.geometry
        self.geom = self.geometry[0]
        #print(self.geom)


    def find_neighs(self):

        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE _st_overlaps(ST_AsText(geom), ST_GeomFromText""" + str(self.geom)[:-2] + "))"

        self.cur.execute(do)
        self.neigh_geometry = self.cur.fetchall()
        #self.con.close()


    def nearby_polygons(self, x, y):

        self.neigh_geometry = self.GIS.ST_DWithin(x, y)

    def process_geometry(self, g):

        print(g)
        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        gTwo = []
        if len(g) < 100:
            input = Proj(init='EPSG:4326')
            output = Proj(init='EPSG:27700')  # output = Proj(init='EPSG:27700')
            for i in range(0, len(g), 2):
                x_temp, y_temp = transform(input, output, g[i], g[i + 1])
                gTwo.append(x_temp)
                gTwo.append(y_temp)

        return gTwo

    def add_to_site_list(self):

        self.site_dict = {}

    def incrementID(self):
        self.id += 1

    def add_to_site_list(self, geometry):

        addressList = []
        addressList.append(self.address)
        temp_dict = {}
        m = [float(item) for item in geometry]
        x_poly, y_poly = [], []
        for j in range(int(len(m) / 2)):
            x_poly.append(round(1000 * m[2 * j]) / 1000)
            y_poly.append(round(1000 * m[2 * j + 1]) / 1000)
        # All polygons have one duplicated point and should be sorted ACW
        if len(x_poly) > 2:
            x_poly, y_poly = self.gt.sort_array_acw(x_poly[1:], y_poly[1:])
        temp_dict['id'] = self.id
        temp_dict['house_address_list'] = addressList
        temp_dict['x'] = self.x1
        temp_dict['y'] = self.y1
        temp_dict['x_poly'] = x_poly
        temp_dict['y_poly'] = y_poly
        temp_dict['geom'] = self.geometry
        temp_dict['org_geom'] = self.geomForDict
        temp_dict['multi_house'] = False
        temp_dict['area'] = abs(self.gt.find_area(x_poly, y_poly))
        temp_dict['neigh_sites'] = []
        self.dict[self.id] = temp_dict

        return temp_dict
