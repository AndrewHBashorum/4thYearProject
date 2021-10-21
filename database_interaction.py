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

class Database(object):
    def __init__(self):

        if user == 'andrew':
            self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD", host="localhost",
                                   port="5432")
        else:
            self.con = psycopg2.connect(database="nps_database_cropped", user="postgres", password="$£x25zeD",
                                        host="localhost", port="5433")

        self.cur = self.con.cursor()

        pass

    def ST_Contains(self, x, y):

        x = x
        y = y

        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE ST_Contains(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")'))"

        self.cur.execute(do)
        geometry = self.cur.fetchall()

        self.ST_Transform(x,y,geometry)
        return geometry

    def ST_DWithin(self, x, y):

        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE _ST_DWithin(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")'),0.0001)"

        # execute the command and fecth geometry
        self.cur.execute(do)
        neigh_geometry = self.cur.fetchall()

        return neigh_geometry

    def ST_Transform(self, x, y, geom):

        do = """SELECT ST_Transform(ST_GeomFromText(""" + str(geom[0].replace(')'), '') + "'),4326)"

        #""""FROM public."nps_cropped_lynmouth"""
        print(do)
        # execute the command and fecth geometry
        self.cur.execute(do)
        geo = self.cur.fetchall()
        print(geo)

        #return neigh_geometry