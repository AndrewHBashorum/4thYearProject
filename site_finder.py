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



    def get_house_dict(self):

        #self.houses.get_houses_os_walk()

        self.houses.sample_house()
        self.houses.geo_locate_houses()

    def checkSitesForDupes(self, geom):

        site_id = None
        for site in self.sites.dict.keys():
            if self.sites.dict[site]['geom'] == geom:
                site_id = site

        return site_id

    def main(self):

        self.get_house_dict()

        for house_ID in self.houses.house_dict.keys():

            self.sites.take_from_database(self.houses.house_dict[house_ID]['Point_original_x'],self.houses.house_dict[house_ID]['Point_original_y'],self.houses.house_dict[house_ID]['Point_converted_x'],self.houses.house_dict[house_ID]['Point_converted_y'],house_ID)
            self.sites.find_neighs()
            #self.sites.nearby_polygons(house_dict[address]['x'], house_dict[address]['y'])
            self.sites.geometry = self.sites.process_geometry(str(self.sites.geom))

            dupeSiteFound_id = self.checkSitesForDupes(self.sites.geometry)
            if dupeSiteFound_id != None:
                print('>>><>', dupeSiteFound_id)
                self.sites.dict[dupeSiteFound_id]['multi_house'] = True
                self.sites.dict[dupeSiteFound_id]['house_address_list'].append(house_ID)
                self.houses.house_dict[house_ID]['sites'].append(dupeSiteFound_id)
            else:
                self.sites.add_to_site_list(self.sites.geometry)
                self.houses.house_dict[house_ID]['sites'].append(self.sites.id)
                self.sites.incrementID()


            for i in self.sites.dict.keys():
                if self.sites.dict[i]['multi_house'] == True:# sel  self.sites.incrementID()
                    for address in self.sites.dict[i]['house_address_list']:
                        splitAdress = address.split('_')
                        number = int(splitAdress[0])
                        # self.houses.house_dict[address]['potential_neighs'].append(str(number + 2) + '_' + splitAdress[1] + '_' + splitAdress[2])
                        # self.houses.house_dict[address]['potential_neighs'].append(str(number - 2) + '_' + splitAdress[1] + '_' + splitAdress[2])
                        # self.houses.house_dict[address]['potential_neighs'].append(str(number + 4) + '_' + splitAdress[1] + '_' + splitAdress[2])
                        # self.houses.house_dict[address]['potential_neighs'].append(str(number - 4) + '_' + splitAdress[1] + '_' + splitAdress[2])

                    print(self.sites.dict[i]['id'])

            # f.sites.neigh_geometry_list = []
            # for j in range(len(self.sites.neigh_geometry)):
            #     new1 = self.sites.process_geometry(str(self.sites.neigh_geometry[j]))
            #     print(new1)
            #     self.sites.neigh_geometry_list.append(new1)
            # print('*', len(self.sites.neigh_geometry_list), self.sites.neigh_geometry_list)






        self.sites.con.close()

        self.SITES = self.sites.SITES
        self.temp_neigh_sites = []
        for g in self.sites.neigh_geometry:
            self.temp_neigh_sites.append(self.sites.process_geometry(g[0]))

        self.plotter()


if __name__ == '__main__':

    sf = SiteFinder()
    sf.main()