# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT

from os import path
from pathlib import Path
import sys
from pyproj import Proj, transform

sys.path.append(path.abspath(str(Path.home())))
sys.path.append(path.abspath(str(Path.home()) + '/4thYearProject'))
if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
else:
    user = 'luke'

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def take_from_database(x, y, PostGIS_fns):
    return PostGIS_fns.ST_Contains(x, y)[0][0]

def find_neighs_overlap(geom, cur):
    do = """SELECT ST_AsText(geom) FROM public."nps_cropped_lynmouth" WHERE _st_overlaps(ST_AsText(geom), ST_GeomFromText('""" + geom + "'))"
    cur.execute(do)
    neigh_geometry = cur.fetchall()
    for i in range(len(neigh_geometry)):
        neigh_geometry[i] = neigh_geometry[i][0]
    return neigh_geometry

def nearby_polygons(x, y, PostGIS_fns, d):
    neigh_geometry = PostGIS_fns.ST_DWithin(x, y, d)
    for i in range(len(neigh_geometry)):
        neigh_geometry[i] = neigh_geometry[i][0]
    return neigh_geometry

def process_geometry(g, gt):
    g = g.replace("MULTIPOLYGON", "")
    g = g.replace("(", "")
    g = g.replace(")", "")
    g = g.replace(",", " ")
    g = g.replace('"', " ")
    g = g.replace("'", " ")
    g = g.split()

    gTwo, x_poly, y_poly = [], [], []
    if len(g) < 100:
        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:27700')
        for i in range(0, len(g), 2):
            x_temp, y_temp = transform(input, output, g[i], g[i + 1])
            gTwo.append(x_temp)
            gTwo.append(y_temp)
            x_poly.append(x_temp)
            y_poly.append(y_temp)
    x_poly, y_poly = gt.sort_array_acw(x_poly[1:], y_poly[1:])
    return gTwo, x_poly, y_poly
