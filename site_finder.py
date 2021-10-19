# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
from geopy.geocoders import GoogleV3
from pyproj import Proj, transform
# from pyproj import Transformer
import os
from os import path
import sys
from pathlib import Path
import psycopg2
import geometry as geo
import matplotlib.pyplot as plt
import time
import pickle
from houses import Houses
from sites import Sites
from geometry import Geometry
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


class SiteFinder(object):
    def __init__(self):
        self.houses = Houses()
        self.sites = Sites()
        self.gt = Geometry()
        pass

    def plotter(self):

        for g in self.temp_neigh_sites:
            if g != []:
                x_temp = []
                y_temp = []
                for i in range(0, len(g), 2):
                    x_temp.append(g[i])
                    y_temp.append(g[i+1])
                aspect_ratio, area = self.gt.get_aspect_ratio_area(x_temp, y_temp)
                print(aspect_ratio, area)
                if area < 1000:
                    plt.fill(x_temp, y_temp, '--', fill=False, color='g')

        for i in range(len(self.SITES)):
            if self.SITES[i]['area'] < 1000:
                plt.plot(self.SITES[i]['x'], self.SITES[i]['y'], 'o', color='r')
                plt.fill(self.SITES[i]['x_poly'], self.SITES[i]['y_poly'], fill=False, color='b')


    def main(self):

        # self.houses.get_houses_os_walk()
        self.houses.sample_house()
        self.houses.geo_locate_houses()
        house_dict = self.houses.house_dict

        for address in house_dict:
            self.sites.take_from_database(house_dict[address]['x'], house_dict[address]['y'], house_dict[address]['x1'], house_dict[address]['y1'], address)
            self.sites.nearby_polygons(house_dict[address]['x'], house_dict[address]['y'])
            self.sites.geometry = self.sites.process_geometry(self.sites.geometry[0][0])
            self.sites.add_to_site_list()

        self.sites.con.close()

        self.SITES = self.sites.SITES
        self.temp_neigh_sites = []
        for g in self.sites.neigh_geometry:
            self.temp_neigh_sites.append(self.sites.process_geometry(g[0]))

        self.plotter()

if __name__ == '__main__':
    sf = SiteFinder()
    sf.main()
    print('*', len(sf.sites.neigh_geometry))