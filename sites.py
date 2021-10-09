import numpy as np
import json
import pickle5 as pickle
import os
from os import path
from pathlib import Path
import matplotlib.pyplot as plt
import sys

from geometry import Geometry
from pyproj import Proj, transform

sys.path.append(path.abspath(str(Path.home())))
sys.path.append(path.abspath(str(Path.home()) + '/4thYearProject'))
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path
import psycopg2

class Sites(object):
    def __init__(self):

        self.gt = Geometry()
        self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD", host="localhost",
                               port="5432")
        self.cur = self.con.cursor()
        self.SITES = []
        pass

    def take_from_database(self,x,y,x1,y1,address):

        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.address = address


        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE ST_Contains(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")'))"

        # execute the command and fecth geometry
        self.cur.execute(do)
        self.geometry = self.cur.fetchall()
        # self.con.close()

    def process_geometry(self):

        g = self.geometry[0][0]
        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.split()

        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:27700')  # output = Proj(init='EPSG:27700')
        gTwo = []
        # for a in range(1, 100, 2):
        for i in range(0, len(g), 2):
            x_temp, y_temp = transform(input, output, g[i], g[i + 1])
            # print(i,x)
            gTwo.append(x_temp)
            gTwo.append(y_temp)
        # get points
        self.geometry = gTwo

    def add_to_site_list(self):

        temp_dict = {}
        m = [float(item) for item in self.geometry]
        x_poly, y_poly = [], []
        for j in range(int(len(m) / 2)):
            x_poly.append(round(1000 * m[2 * j]) / 1000)
            y_poly.append(round(1000 * m[2 * j + 1]) / 1000)
        # All polygons have one duplicated point and should be sorted ACW
        if len(x_poly) > 2:
            x_poly, y_poly = self.gt.sort_array_acw(x_poly[1:], y_poly[1:])
        temp_dict['name'] = self.address
        temp_dict['x'] = self.x1
        temp_dict['y'] = self.y1
        temp_dict['x_poly'] = x_poly
        temp_dict['y_poly'] = y_poly
        temp_dict['area'] = abs(self.gt.find_area(x_poly, y_poly, sum(x_poly) / len(x_poly), sum(y_poly) / len(y_poly)))
        self.SITES.append(temp_dict)
