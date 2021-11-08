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
from sites_utils import take_from_database, find_neighs_overlap, nearby_polygons, process_geometry
from geometry import Geometry
from database_interaction import Database

from datetime import date
import psycopg2
from site_object import SiteObject

import time

class SiteFinder(object):

    def __init__(self):
        self.gt = Geometry()
        self.house_dict = {}
        self.site_dict = {}
        self.neigh_site_dict = {}

    def plotter(self):
        plt.figure()
        for i in self.neigh_site_dict.keys():
            if self.neigh_site_dict[i].active:
                x_poly = self.neigh_site_dict[i].x_poly
                y_poly = self.neigh_site_dict[i].y_poly
                plt.fill(x_poly, y_poly, ':', fill=False, color='r', linewidth=3)

        for i in self.site_dict.keys():
            plt.fill(self.site_dict[i].x_poly, self.site_dict[i].y_poly, fill=False, color='b')
            # plt.plot(self.site_dict[i].x_poly, self.site_dict[i].y_poly, ':', color='b')
            if self.site_dict[i].multi_house:
                print('*',i)

        for i in self.house_dict.keys():
            plt.plot(self.house_dict[i].xt, self.house_dict[i].yt, 'o', color='r')

    def checkSitesForDupes(self, geom, dict):
        site_id = None
        for site_temp in dict.keys():
            if dict[site_temp].geom == geom:
                site_id = site_temp

        return site_id

    def checkSitesForDupesGTwo(self, gTwo, dict):
        site_id = None
        for site_temp in dict.keys():
            if dict[site_temp].gTwo == gTwo:
                site_id = site_temp

        return site_id

    def fix_site_duplicate(self):

        self.PostGIS_fns = Database()
        site_keys = self.site_dict.keys()
        site_object_list = []
        num_sites = len(self.site_dict)
        for k in site_keys:
            if sf.site_dict[k].multi_house:
                house_address_list = self.site_dict[k].house_address_list

                # 2 houses in one site
                if len(house_address_list) == 2:
                    house_numbers = []
                    house_ids = []
                    sites = []
                    sites_geom = []
                    sites.append(self.site_dict[k].gTwo)
                    sites_geom.append(self.site_dict[k].geom_27700)
                    sites.append(self.site_dict[k].neigh_sites[0])
                    sites_geom.append(self.neigh_site_dict[self.site_dict[k].neigh_sites_id[0]].geom_27700)
                    for h in house_address_list:
                        splitAddress = h.split('_')
                        house_numbers.append(int(splitAddress[0]))
                        house_ids.append(h)
                    pre_house = min(house_numbers) - 2
                    pre_house_id = [x for x in list(self.house_dict.keys()) if str(pre_house) + '_' in x]
                    post_house = max(house_numbers) + 2
                    post_house_id = [x for x in list(self.house_dict.keys()) if str(post_house) + '_' in x]
                    if len(pre_house_id) > 0:
                        house_numbers = [pre_house] + house_numbers
                        house_ids = [pre_house_id[0]] + house_ids
                        sites = [self.site_dict[self.house_dict[pre_house_id[0]].sites[0]].gTwo] + sites
                        sites_geom = [self.site_dict[self.house_dict[pre_house_id[0]].sites[0]].geom_27700] + sites_geom
                    if len(post_house_id) > 0:
                        house_numbers.append(post_house)
                        house_ids.append(post_house_id[0])
                        sites.append(self.site_dict[self.house_dict[post_house_id[0]].sites[0]].gTwo)
                        sites_geom.append(self.site_dict[self.house_dict[post_house_id[0]].sites[0]].geom_27700)

                    d1 = self.PostGIS_fns.centre_site_to_dist(sites[0], sites[1])
                    d1 += self.PostGIS_fns.centre_site_to_dist(sites[1], sites[2])
                    d1 += self.PostGIS_fns.centre_site_to_dist(sites[2], sites[3])
                    d2 = self.PostGIS_fns.centre_site_to_dist(sites[0], sites[2])
                    d2 += self.PostGIS_fns.centre_site_to_dist(sites[2], sites[1])
                    d2 += self.PostGIS_fns.centre_site_to_dist(sites[1], sites[3])
                    # d1 = self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[0], sites_geom[1]))
                    # d1 += self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[1], sites_geom[2]))
                    # d1 += self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[2], sites_geom[3]))
                    # d2 = self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[0], sites_geom[2]))
                    # d2 += self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[2], sites_geom[1]))
                    # d2 += self.PostGIS_fns.linestring_to_length(self.PostGIS_fns.ST_ShortestLine(sites_geom[1], sites_geom[3]))

                    print(d1, d2)

                    if d1 < d2:
                        id1 = house_ids[1]
                        id2 = house_ids[2]
                        sid1 = 1
                        sid2 = 2
                    else:
                        id1 = house_ids[2]
                        id2 = house_ids[1]
                        sid1 = 2
                        sid2 = 1

                    # change site_ob
                    self.site_dict[k].house_address_list = id1
                    self.site_dict[k].multi_house = False

                    # make new site ob
                    gTwo = sites[sid2]
                    x_poly = []
                    y_poly = []
                    for i in range(0, len(gTwo), 2):
                        x_poly.append(float(gTwo[i]))
                        y_poly.append(float(gTwo[i + 1]))

                    site_ob = SiteObject()
                    num_sites += 1
                    site_ob.id = num_sites
                    site_ob.xt = sum(x_poly) / max(1, len(x_poly))
                    site_ob.yt = sum(y_poly) / max(1, len(y_poly))
                    site_ob.x_poly = x_poly
                    site_ob.y_poly = y_poly
                    site_ob.gTwo = gTwo
                    site_ob.house_address_list = house_ids[sid2]
                    aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(x_poly, y_poly)
                    site_ob.aspect_ratio = aspect_ratio
                    site_ob.orientation = orientation
                    site_ob.geom = self.neigh_site_dict[k].geom
                    site_ob.geom_27700 = self.neigh_site_dict[k].geom_27700
                    site_ob.multi_house = False
                    site_ob.area = abs(self.gt.find_area(x_poly, y_poly))
                    site_ob.neigh_sites = []
                    site_object_list.append(site_ob)

                    # change second house
                    self.house_dict[id2].xt = site_ob.xt
                    self.house_dict[id2].yt = site_ob.yt
                    self.house_dict[id2].sites = [site_ob.id]

        if len(site_object_list) > 0:
            num_sites = len(self.site_dict)
            for i in range(len(site_object_list)):
                self.site_dict[num_sites + i + 1] = site_object_list[i]

    def main(self, case):
        print('Getting house dict....')
        if case == 1:
            house_addresses = ['67 Lynmouth Dr Ruislip HA4 9BY UK','51 Lynmouth Dr Ruislip HA4 9BY UK']
        elif case == 2:
            house_addresses = get_houses_os_walk()
        elif case == 3:
            house_addresses = spreadsheet_input('LynmouthDriveOdd')

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
                print('Duplicate Found for ID:', dupeSiteFound_id)
                self.site_dict[dupeSiteFound_id].multi_house = True
                self.site_dict[dupeSiteFound_id].house_address_list.append(house_ID)
                self.house_dict[house_ID].sites.append(dupeSiteFound_id)
                for ng in neigh_geom_dist:
                    gTwo_ng, x_poly_ng, y_poly_ng = process_geometry(ng, self.gt)
                    aspect_ratio_ng, area_ng, orientation_ng = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                    if abs(orientation_ng - orientation) < 0.1 and area_ng > 35 and area_ng < 1000 and gTwo_ng != gTwo:
                        self.site_dict[dupeSiteFound_id].neigh_sites.append(gTwo_ng)
            else:
                self.id += 1
                site_ob = SiteObject()
                site_ob.id = self.id
                site_ob.xt = sum(x_poly)/max(1, len(x_poly))
                site_ob.yt = sum(y_poly)/max(1, len(y_poly))
                site_ob.x_poly = x_poly
                site_ob.y_poly = y_poly
                site_ob.gTwo = gTwo
                aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(x_poly, y_poly)
                site_ob.aspect_ratio = aspect_ratio
                site_ob.orientation = orientation
                site_ob.geom = geom
                site_ob.geom_27700 = self.PostGIS_fns.ST_Transform(geom)
                site_ob.multi_house = False
                site_ob.area = abs(self.gt.find_area(x_poly, y_poly))
                site_ob.neigh_sites = []
                self.site_dict[self.id] = site_ob
                self.site_dict[self.id].house_address_list.append(house_ID)
                self.house_dict[house_ID].sites.append(self.id)
                for ng in neigh_geom_dist:
                    gTwo_ng, x_poly_ng, y_poly_ng = process_geometry(ng, self.gt)
                    aspect_ratio_ng, area_ng, orientation_ng = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                    # ng_dupeSiteFound_id = self.checkSitesForDupesGTwo(gTwo_ng, self.site_dict)
                    if abs(orientation_ng - orientation) < 0.1 and area_ng > 35 and area_ng < 1000 and gTwo_ng != gTwo:# and ng_dupeSiteFound_id == None:
                        self.site_dict[self.id].neigh_sites.append(gTwo_ng)

            for ng in neigh_geom_dist:
                ng_dupeSiteFound_id_1 = self.checkSitesForDupes(ng, self.neigh_site_dict)
                ng_dupeSiteFound_id_2 = self.checkSitesForDupes(ng, self.site_dict)
                if ng_dupeSiteFound_id_1 == None and ng_dupeSiteFound_id_2 == None:
                    gTwo_ng, x_poly_ng, y_poly_ng = process_geometry(ng, self.gt)
                    aspect_ratio_ng, area_ng, orientation_ng = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                    if abs(orientation_ng - orientation) < 0.1 and area_ng > 35 and area_ng < 1000:
                        self.neigh_id += 1
                        n_site_ob = SiteObject()
                        n_site_ob.id = self.neigh_id
                        n_site_ob.xt = sum(x_poly_ng)/max(1, len(x_poly_ng))
                        n_site_ob.yt = sum(y_poly_ng)/max(1, len(y_poly_ng))
                        n_site_ob.x_poly = x_poly_ng
                        n_site_ob.y_poly = y_poly_ng
                        n_site_ob.gTwo = gTwo_ng
                        n_site_ob.geom = ng
                        n_site_ob.geom_27700 = self.PostGIS_fns.ST_Transform(ng)
                        self.neigh_site_dict[self.neigh_id] = n_site_ob

        for k in self.neigh_site_dict.keys():
            ng = self.neigh_site_dict[k].gTwo
            ng_dupeSiteFound_id_1 = self.checkSitesForDupesGTwo(ng, self.site_dict)
            if ng_dupeSiteFound_id_1 != None:
                self.neigh_site_dict[k].active = False

        for k in self.site_dict.keys():
            ng_gtwo_list = self.site_dict[k].neigh_sites
            ng_gtwo_list_temp = []
            neigh_sites_id = []
            for ng in ng_gtwo_list:
                ng_dupeSiteFound_id_1 = self.checkSitesForDupesGTwo(ng, self.site_dict)
                ng_dupeSiteFound_id_2 = self.checkSitesForDupesGTwo(ng, self.neigh_site_dict)
                x,y = [], []
                if ng_dupeSiteFound_id_1 == None:
                    ng_gtwo_list_temp.append(ng)
                    neigh_sites_id.append(ng_dupeSiteFound_id_2)
            self.site_dict[k].neigh_sites = [list(x) for x in set(tuple(x) for x in ng_gtwo_list_temp)]
            self.site_dict[k].neigh_sites_id = list(set(neigh_sites_id))

        self.fix_site_duplicate()
        self.plotter()

    def main_from_pickle(self):
        with open('site_finder_lynmouth_odd.pickle', 'rb') as f:
            loadedDict = pickle.load(f)
        self.site_dict = loadedDict['site_dict']
        self.neigh_site_dict = loadedDict['neigh_site_dict']
        self.house_dict = loadedDict['house_dict']

        self.fix_site_duplicate()
        self.plotter()

if __name__ == '__main__':
    start = time.time()
    load_from_pickle = True
    sf = SiteFinder()
    if load_from_pickle:
        sf.main_from_pickle()
        # dict = {
        #     'house_dict': sf.house_dict,
        #     'site_dict': sf.site_dict,
        #     'neigh_site_dict': sf.neigh_site_dict
        # }
        # with open('site_finder_lynmouth_odd.pickle', 'wb') as f:
        #     pickle.dump(dict, f)
    else:
        sf.main(3)
        date = today = date.today()
        dict = {
            'house_dict': sf.house_dict,
            'site_dict': sf.site_dict,
            'neigh_site_dict': sf.neigh_site_dict
        }
        with open('site_finder_lynmouth_odd.pickle', 'wb') as f:
            pickle.dump(dict, f)
    gt = Geometry()
    # for k in sf.house_dict.keys():
    #     x, y = sf.house_dict[k].xt, sf.house_dict[k].yt
    #     site_id = sf.house_dict[k].sites[0]
    #     x_poly, y_poly = sf.site_dict[site_id].x_poly, sf.site_dict[site_id].y_poly
    #     print(k, site_id, gt.point_in_polygon(x, y, x_poly, y_poly))

    end = time.time()
    keys = sf.house_dict.keys()

    print('Time Taken:', round(end - start), 'seconds')

    # for i in self.sites.dict.keys():
    #     if self.sites.dict[i]['multi_house'] == True:# sel  self.sites.incrementID()
    #         for address in self.sites.dict[i]['house_address_list']:
    #             splitAddress = address.split('_')
    #             number = int(splitAddress[0])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number + 2) + '_' + splitAddress[1] + '_' + splitAddress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number - 2) + '_' + splitAddress[1] + '_' + splitAddress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number + 4) + '_' + splitAddress[1] + '_' + splitAddress[2])
    #             # self.houses.house_dict[address]['potential_neighs'].append(str(number - 4) + '_' + splitAddress[1] + '_' + splitAddress[2])
    #
    #         print(self.sites.dict[i]['id'])
