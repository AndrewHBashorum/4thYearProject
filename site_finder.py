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
import pickle5 as pickle
from houses import Houses
from sites import Sites
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
class SiteFinder(object):

    def __init__(self):

        self.houses = Houses()
        self.sites = Sites()

        pass

    def plotter(self):

        for i in range(len(self.SITES)):
            if self.SITES[i]['area'] < 1000:
                plt.plot(self.SITES[i]['x'], self.SITES[i]['y'], 'o', color='r')
                plt.fill(self.SITES[i]['x_poly'], self.SITES[i]['y_poly'], fill=False, color='b')

        for i in range(len(self.NEIGH_SITES)):
            plt.fill(self.NEIGH_SITES[i]['x_poly'], self.NEIGH_SITES[i]['y_poly'], ':', fill=False, color='g')

    def main(self):

        #self.houses.get_houses_os_walk()
        self.houses.sample_house()
        self.houses.geo_locate_houses()

        house_dict = self.houses.house_dict

        for address in house_dict:
            self.sites.take_from_database(house_dict[address]['x'],house_dict[address]['y'],house_dict[address]['x1'],house_dict[address]['y1'],address)
            self.sites.find_neighs()
            self.sites.geometry = self.sites.process_geometry(str(self.sites.geom))

            self.sites.neigh_geometry_list = []
            for j in range(len(self.sites.neigh_geometry)):
                new1 = self.sites.process_geometry(str(self.sites.neigh_geometry[j]))
                print(new1)
                self.sites.neigh_geometry_list.append(new1)
            print('*', len(self.sites.neigh_geometry_list), self.sites.neigh_geometry_list)
            # self.sites.add_to_site_list()

        self.SITES = []
        self.SITES.append(self.sites.add_to_site_list(self.sites.geometry))

        self.NEIGH_SITES = []
        for j in range(len(self.sites.neigh_geometry_list)):
            print('*', j)
            self.NEIGH_SITES.append(self.sites.add_to_site_list(self.sites.neigh_geometry_list[j]))

        self.plotter()


if __name__ == '__main__':

    sf = SiteFinder()
    sf.main()