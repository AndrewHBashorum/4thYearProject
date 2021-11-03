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
from sites_utils import take_from_database, find_neighs, nearby_polygons, process_geometry
from geometry import Geometry
from database_interaction import Database

from datetime import date
import psycopg2
from site_object import SiteObject

class SiteFinder(object):

    def __init__(self):
        self.gt = Geometry()
        self.house_dict = {}
        self.site_dict = {}
        self.neigh_site_dict = {}

    def plotter(self):
        for i in self.site_dict.keys():
            for g in self.site_dict[i].neigh_sites:
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

        for i in self.site_dict.keys():
            if self.site_dict[i].area < 1000:
                plt.plot(self.site_dict[i].x, self.site_dict[i].y, 'o', color='r')
                plt.fill(self.site_dict[i].x_poly, self.site_dict[i].y_poly, fill=False, color='b')

    def checkSitesForDupes(self, geom, dict):
        site_id = None
        for site in dict.keys():
            if dict[site].geom == geom:
                site_id = site

        return site_id

    def main(self, case):
        print('Getting house dict....')
        if case == 1:
            house_addresses = ['67 Lynmouth Dr Ruislip HA4 9BY UK','51 Lynmouth Dr Ruislip HA4 9BY UK']
        elif case == 2:
            house_addresses = get_houses_os_walk()
        elif case == 3:
            house_addresses = spreadsheet_input('LynmouthDriveOdd')
        elif case == 4:
            house_addresses = get_houses_from_pickle()
        for h in house_addresses:
            print(h)
        self.house_dict = geo_locate_houses(house_addresses, self.house_dict)
        print('....House dict obtained')
        self.id = 0
        self.neigh_id = 0
        if user == 'andrew':
            self.con = psycopg2.connect(database="sdb_course", user="postgres", password="$£x25zeD",
                                        host="localhost", port="5432")
        else:
            self.con = psycopg2.connect(database="nps_database_cropped", user="postgres", password="$£x25zeD",
                                        host="localhost", port="5433")
        self.cur = self.con.cursor()
        self.PostGIS_fns = Database()

        for house_ID in self.house_dict.keys():
            print(house_ID)
            geom = take_from_database(self.house_dict[house_ID].xd, self.house_dict[house_ID].yd, self.PostGIS_fns)
            # neigh_geom_contact = find_neighs(geom, self.cur)
            neigh_geom_dist = nearby_polygons(self.house_dict[house_ID].xd, self.house_dict[house_ID].yd, self.PostGIS_fns, 0.0001)
            gTwo, x_poly, y_poly = process_geometry(geom, self.gt)
            dupeSiteFound_id = self.checkSitesForDupes(geom, self.site_dict)

            if dupeSiteFound_id != None:
                print('Dupelicate Found for ID:', dupeSiteFound_id)
                self.site_dict[dupeSiteFound_id].multi_house = True
                self.site_dict[dupeSiteFound_id].house_address_list.append(house_ID)
                self.house_dict[house_ID].sites.append(dupeSiteFound_id)
                for ng in neigh_geom_dist:
                    gTwo, x_poly, y_poly = process_geometry(ng, self.gt)
                    self.site_dict[dupeSiteFound_id].neigh_sites.append(gTwo)
            else:
                self.id += 1
                site_object = SiteObject()
                site_object.id = self.id
                site_object.x = self.house_dict[house_ID].xt
                site_object.y = self.house_dict[house_ID].yt
                site_object.x_poly = x_poly
                site_object.y_poly = y_poly
                site_object.geom = geom
                site_object.geom_27700 = self.PostGIS_fns.ST_Transform(geom)
                site_object.multi_house = False
                site_object.area = abs(self.gt.find_area(x_poly, y_poly))
                site_object.neigh_sites = []
                self.site_dict[self.id] = site_object
                self.house_dict[house_ID].sites.append(self.id)
                for ng in neigh_geom_dist:
                    gTwo, x_poly, y_poly = process_geometry(ng, self.gt)
                    self.site_dict[self.id].neigh_sites.append(gTwo)

            for ng in neigh_geom_dist:
                ng_dupeSiteFound_id_1 = self.checkSitesForDupes(ng, self.neigh_site_dict)
                ng_dupeSiteFound_id_2 = self.checkSitesForDupes(ng, self.site_dict)
                if ng_dupeSiteFound_id_1 == None and ng_dupeSiteFound_id_2 == None:
                    gTwo_ng, x_poly_ng, y_poly_ng = process_geometry(ng, self.gt)
                    self.neigh_id += 1
                    n_site_object = SiteObject()
                    n_site_object.id = self.neigh_id
                    n_site_object.x = sum(x_poly_ng)/max(1, len(x_poly_ng))
                    n_site_object.y = sum(y_poly_ng)/max(1, len(y_poly_ng))
                    n_site_object.x_poly = x_poly_ng
                    n_site_object.y_poly = y_poly
                    n_site_object.geom = ng
                    n_site_object.geom_27700 = self.PostGIS_fns.ST_Transform(ng)
                    self.neigh_site_dict[self.neigh_id] = n_site_object
        self.plotter()

    def main_from_pickle(self):
        with open('site_finder_luke.pickle', 'rb') as f:
            loadedDict = pickle.load(f)
        self.site_dict = loadedDict['site_dict']
        self.neigh_site_dict = loadedDict['neigh_site_dict']
        self.house_dict = loadedDict['house_dict']
        self.plotter()

if __name__ == '__main__':

    load_from_pickle = True
    sf = SiteFinder()
    if load_from_pickle:
        sf.main_from_pickle()
    else:
        sf.main(1)
        date = today = date.today()
        dict = {
            'house_dict': sf.house_dict,
            'site_dict': sf.site_dict,
            'neigh_site_dict': sf.neigh_site_dict
        }

        with open('site_finder_luke.pickle', 'wb') as f:
            pickle.dump(dict, f)

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
