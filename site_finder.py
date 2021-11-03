# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT

from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    import pickle5 as pickle
else:
    user = 'luke'
    import pickle

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import matplotlib.pyplot as plt

from houses_utils import get_houses_os_walk, spreadsheet_input, get_houses_from_pickle, geo_locate_houses
from sites import Sites
from geometry import Geometry
from datetime import date

class SiteFinder(object):

    def __init__(self):
        self.sites = Sites()
        self.gt = Geometry()

        self.house_dict = {}
        self.site_dict = {}
        self.neigh_site_dict = {}

        pass

    def plotter(self):
        for i in self.sites.dict.keys():
            for g in self.sites.dict[i].neigh_sites:
                if g != []:
                    x_temp = []
                    y_temp = []
                    for j in range(0, len(g), 2):
                        x_temp.append(g[j])
                        y_temp.append(g[j+1])
                    aspect_ratio, area = self.gt.get_aspect_ratio_area(x_temp, y_temp)
                    print(aspect_ratio, area)
                    if area < 1000:
                        plt.fill(x_temp, y_temp, '--', fill=False, color='g')

        for i in range(len(self.sites.dict)):
            if self.sites.dict[i].area < 1000:
                plt.plot(self.sites.dict[i].x, self.sites.dict[i].y, 'o', color='r')
                plt.fill(self.sites.dict[i].x_poly, self.sites.dict[i].y_poly, fill=False, color='b')

    def get_house_dict(self):

        house_addresses = ['67 Lynmouth Dr Ruislip HA4 9BY UK']
        # house_addresses = get_houses_os_walk()
        # house_addresses = spreadsheet_input('LynmouthDriveOdd')
        # house_addresses = get_houses_from_pickle()
        for h in house_addresses:
            print(h)

        self.house_dict = geo_locate_houses(house_addresses, self.house_dict)

    def checkSitesForDupes(self, geom):

        site_id = None
        for site in self.sites.dict.keys():
            if self.sites.dict[site].geom == geom:
                site_id = site

        return site_id

    def main(self):

        print('Getting house dict....')
        self.get_house_dict()
        print('....House dict obtained')
        #house_ID = '67_HA4_9BY'
        #house_ID = '35_HA4_9BY'
        # self.sites.take_from_database(self.houses.house_dict[house_ID]['Point_original_x'],
        #                               self.houses.house_dict[house_ID]['Point_original_y'],
        #                               self.houses.house_dict[house_ID]['Point_converted_x'],
        #                               self.houses.house_dict[house_ID]['Point_converted_y'], house_ID)
        """
        for house_ID in self.houses.house_dict.keys():

            self.sites.take_from_database(self.houses.house_dict[house_ID].Point_original_x, self.houses.house_dict[house_ID].Point_original_y,
                                          self.houses.house_dict[house_ID].Point_converted_x, self.houses.house_dict[house_ID].Point_converted_y, house_ID)
            self.sites.find_neighs()
            self.sites.nearby_polygons(self.houses.house_dict[house_ID].Point_original_x, self.houses.house_dict[house_ID].Point_original_y)
            self.sites.geometry = self.sites.process_geometry(str(self.sites.geom))

            dupeSiteFound_id = self.checkSitesForDupes(self.sites.geometry)
            if dupeSiteFound_id != None:
                print('Dupelicate Found for ID:', dupeSiteFound_id)
                self.sites.dict[dupeSiteFound_id].multi_house = True
                self.sites.dict[dupeSiteFound_id].house_address_list.append(house_ID)
                self.houses.house_dict[house_ID].sites.append(dupeSiteFound_id)
                for g in self.sites.neigh_geometry:
                    self.sites.dict[dupeSiteFound_id].neigh_sites.append(self.sites.process_geometry(g[0]))
            else:
                self.sites.add_to_site_list(self.sites.geometry)
                self.houses.house_dict[house_ID].sites.append(self.sites.id)
                for g in self.sites.neigh_geometry:
                    self.sites.dict[self.sites.id].neigh_sites.append(self.sites.process_geometry(g[0]))
                self.sites.incrementID()

            print('Site ID:',self.sites.id)

        self.sites.con.close()
        self.plotter()"""

    def main_from_pickle(self):

        with open('site_finder.pickle', 'rb') as f:
            loadedDict = pickle.load(f)

        self.sites.dict = loadedDict['site_dict']
        self.houses.house_dict = loadedDict['house_dict']
        self.plotter()

if __name__ == '__main__':

    load_from_pickle = False
    sf = SiteFinder()

    if load_from_pickle:
        sf.main_from_pickle()
    else:
        sf.main()
        # date = today = date.today()
        # dict = {
        #     'house_dict': sf.houses.house_dict,
        #     'site_dict': sf.sites.dict
        # }
        #
        # with open('site_finder.pickle', 'wb') as f:
        #     pickle.dump(dict, f)

    # for i in self.sites.dict.keys():
    #     if self.sites.dict[i]['multi_house'] == True:# sel  self.sites.incrementID()
    #         for address in self.sites.dict[i]['house_address_list']:
    #             splitAdress = address.split('_')
    #             number = int(splitAdress[0])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number + 2) + '_' + splitAdress[1] + '_' + splitAdress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number - 2) + '_' + splitAdress[1] + '_' + splitAdress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number + 4) + '_' + splitAdress[1] + '_' + splitAdress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number - 4) + '_' + splitAdress[1] + '_' + splitAdress[2])
    #
    #         print(self.sites.dict[i]['id'])
