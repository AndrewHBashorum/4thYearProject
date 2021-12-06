# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT

from os import path
from pathlib import Path
import sys
import numpy as np

sys.path.append(path.abspath(str(Path.home())))
sys.path.append(path.abspath(str(Path.home()) + '/4thYearProject'))
if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
else:
    user = 'luke'
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import psycopg2

class Database(object):
    def __init__(self):
        if user == 'andrew':
            self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD", host="localhost", port="5432")
        else:
            self.con = psycopg2.connect(database="nps_database_cropped", user="postgres", password="$£x25zeD", host="localhost", port="5433")
        self.cur = self.con.cursor()

    def ST_Contains(self, x, y):
        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE ST_Contains(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")'))"
        self.cur.execute(do)
        return self.cur.fetchall()

    def single_spatial_to_string(self, geom):
        geom = geom.replace('MULTIPOLYGON','')
        geom = geom.replace('(', '')
        geom = geom.replace(')', '')
        geom = geom.replace(',', '')
        geom = geom.replace('"', '')
        geom = geom.replace('', '')

        return geom

    def single_spatial_to_list(self, g):

        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        return g

    def list_to_single_spatial(self, theList):

        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(theList), 2):
            if i == len(theList) - 2:
                multi_string = multi_string + str(theList[i]) + ' ' + str(theList[i + 1])
            else:
                multi_string = multi_string + str(theList[i]) + ' ' + str(theList[i + 1]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end

        return final_multi

    def x_y_list_to_single_spatial(self, x, y):

        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(x)):
            if i == len(y) - 1:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i])
            else:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end
        f = self.ST_Transform_4326(final_multi)

        return f

    def x_y_list_to_single_spatial_27700(self, x, y):

        multi_string_start = 'MULTIPOLYGON((('
        multi_string_end = ')))'
        multi_string = ''
        for i in range(0, len(x)):
            if i == len(y) - 1:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i])
            else:
                multi_string = multi_string + str(x[i]) + ' ' + str(y[i]) + ','
        final_multi = multi_string_start + multi_string + multi_string_end

        return final_multi

    def single_spatial_to_x_y_list(self, geom):

        g = self.ST_Transform(geom)
        g = g.replace("MULTIPOLYGON", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()

        x_list = []
        y_list = []
        for i in range(0, len(g), 2):
            x_list.append(float(g[i]))
            y_list.append(float(g[i+1]))
        return x_list, y_list

    def ST_DWithin(self, x, y, d):

        do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE _ST_DWithin(ST_AsText(geom), ST_GeomFromText('POINT(""" + str(
            x) + " " + str(y) + ")')," + str(d) + ")"
        self.cur.execute(do)
        neigh_geometry = self.cur.fetchall()
        return neigh_geometry

    def ST_Transform(self, geom):

        do = """SELECT ST_AsText(ST_Transform(ST_GeomFromText(""" + "'" + geom + "',4326), 27700)) As wgs_geom"
        self.cur.execute(do)
        geo = self.cur.fetchall()[0][0]
        return geo

    def ST_Transform_4326(self, geom):

        do = """SELECT ST_AsText(ST_Transform(ST_GeomFromText(""" + "'" + geom + "',27700), 4326)) As wgs_geom"
        self.cur.execute(do)
        geo = self.cur.fetchall()[0][0]
        return geo

    def ST_Area(self, geom):

        do = """SELECT ST_Area(ST_GeomFromText(""" + "'" + geom + "'))"
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_Convex(self, geom):

        do = """SELECT ST_AsText(ST_ConvexHull(ST_GeomFromText(""" + "'" + geom + "'))) As wgs_geom "
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_Concave(self, geom, target_percentage = None):

        if target_percentage == None:
            target_percentage = "0.8"
        do = """SELECT ST_AsText(ST_ConcaveHull(ST_GeomFromText(""" + "'" + geom + "'), """ + target_percentage + """)) As wgs_geom """""
        self.cur.execute(do)
        geo = self.cur.fetchall()
        return geo

    def ST_ShortestLine(self, geom, geom2=None):

        do = """SELECT ST_AsText(ST_ShortestLine(ST_GeomFromText(""" + "'" + geom + "'), """+"ST_GeomFromText(" + "'" + geom2 + "')))"""
        self.cur.execute(do)
        geo = self.cur.fetchall()[0][0]
        return geo

    def linestring_to_length(self, geo):
        g = self.ST_Transform(geo)
        g = g.replace("LINESTRING", "")
        g = g.replace("(", "")
        g = g.replace(")", "")
        g = g.replace(",", " ")
        g = g.replace('"', " ")
        g = g.replace("'", " ")
        g = g.split()
        x_list = []
        y_list = []
        for i in range(0, len(g), 2):
            x_list.append(float(g[i]))
            y_list.append(float(g[i + 1]))
        return np.sqrt((x_list[0] - x_list[1])**2 + (y_list[0] - y_list[1])**2)

    def centre_site_to_dist(self, g1, g2):
        x1, y1 = [] , []
        for i in range(0, len(g1), 2):
            x1.append(float(g1[i]))
            y1.append(float(g1[i + 1]))
        cx1, cy1 = sum(x1)/max(1, len(x1)), sum(y1)/max(1, len(y1))
        x2, y2 = [] , []
        for i in range(0, len(g2), 2):
            x2.append(float(g2[i]))
            y2.append(float(g2[i + 1]))
        cx2, cy2 = sum(x2)/max(1, len(x2)), sum(y2)/max(1, len(y2))
        return np.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)


    def close_connection(self):
        self.con.close()