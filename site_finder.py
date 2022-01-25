# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT

from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    import pickle5 as pickle
    pickle_file_folder = '/Users/andrewbashorum/Dropbox/auto_processing/pickle_files/'
    excel_file_folder = '/Users/andrewbashorum/Dropbox/auto_processing/excel_files/'
else:
    user = 'luke'
    import pickle
    pickle_file_folder = '/Users/lukecoburn/Dropbox/auto_processing/pickle_files/'
    excel_file_folder = '/Users/lukecoburn/Dropbox/auto_processing/excel_files/'

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import matplotlib.pyplot as plt
import numpy as np
import openpyxl

from houses_utils import get_houses_os_walk, spreadsheet_input, get_houses_from_pickle, geo_locate_houses
from sites_utils import take_from_database, find_neighs_overlap, nearby_polygons, process_geometry
from geometry import Geometry
from database_interaction import Database

from datetime import date
import psycopg2
from site_object import SiteObject

import time

class SiteFinder(object):
    def __init__(self, pickle_file_folder=None, excel_file_folder=None):
        self.gt = Geometry()
        self.house_dict = {}
        self.site_dict = {}
        self.neigh_site_dict = {}
        self.pickle_file_folder = pickle_file_folder
        self.excel_file_folder = excel_file_folder

    def plotter(self, tab_str):
        plt.figure()

        for i in self.site_dict.keys():
            plt.fill(self.site_dict[i].x_poly, self.site_dict[i].y_poly, fill=False, color='b')
            plt.fill(self.site_dict[i].x_poly, self.site_dict[i].y_poly, fill=True, color='lightblue')

        for i in self.site_dict.keys():
            plt.plot(self.site_dict[i].xt, self.site_dict[i].yt, '.',color='r')

        for i in self.house_dict.keys():
            text = i.split('_')[0]
            plt.text(self.house_dict[i].xt, self.house_dict[i].yt, text)

        plt.title('Geolocation before correction (' + tab_str + ')')
        plt.ticklabel_format(axis='both', style='sci')
        plt.xlabel('Longitude (EPSG:27700)')
        plt.ylabel('Latitude (EPSG:27700)')

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

    def get_sorted_site_lists(self):
        house_numbers = []
        house_site_numbers = []
        for house_id in self.house_keys:
            house_num = int(house_id.split('_')[0])
            house_numbers.append(house_num)
            temp_str = str(house_num) + '_'
            house_site_num = None
            for site_id in self.site_keys:
                for h in self.site_dict[site_id].house_address:
                    if h[:len(temp_str)] == temp_str:
                        house_site_num = site_id
            house_site_numbers.append(house_site_num)

        x_centre, y_centre = [], []
        for k in self.site_keys:
            x_temp = self.site_dict[k].x_poly
            y_temp = self.site_dict[k].y_poly
            x_centre.append(sum(x_temp)/max(1, len(x_temp)))
            y_centre.append(sum(y_temp)/max(1, len(x_temp)))

        theta = self.gt.linear_regression_to_angle(x_centre, y_centre)
        x_centre, y_centre = self.gt.rotate_polygon(x_centre, y_centre, -theta)
        sort_index = np.argsort(x_centre)
        sorted_site_keys = [self.site_keys[x] for x in sort_index]

        return house_numbers, house_site_numbers, sort_index, sorted_site_keys

    def get_min_distance_from_site_to_other_sites(self, n_site_id):
        min_d = 100000
        x1 = self.neigh_site_dict[n_site_id].x_poly
        y1 = self.neigh_site_dict[n_site_id].y_poly
        for site_id in self.site_keys:
            x2 = self.site_dict[site_id].x_poly
            y2 = self.site_dict[site_id].y_poly
            min_d = self.gt.minimum_pt_pt_dist(x1, y1, x2, y2, min_d)
        return min_d

    def move_second_house_in_site_to_nearest_empty(self, sorted_site_keys):
        radius = 5
        for site_id in self.site_keys:
            if self.site_dict[site_id].num_houses == 2:
                house_addresses = []
                house_numbers = []
                for h in self.site_dict[site_id].house_address:
                    house_numbers.append(int(h.split('_')[0]))
                    house_addresses.append(h)
                h_index = np.argsort(house_numbers)
                house_numbers = [house_numbers[x] for x in h_index]
                house_addresses = [house_addresses[x] for x in h_index]
                ind = sorted_site_keys.index(site_id)
                for i in range(1, radius):
                    index1 = ind + i
                    index2 = ind - i
                    if index1 < len(sorted_site_keys) and not self.site_dict[sorted_site_keys[index1]].num_houses:
                        self.modify_site_and_house_dict_after_double(index1, 0, 1, site_id, sorted_site_keys, house_addresses)
                        break
                    elif index2 > 0 and not self.site_dict[sorted_site_keys[index2]].num_houses:
                        self.modify_site_and_house_dict_after_double(index2, 1, 0, site_id, sorted_site_keys, house_addresses)
                        break

    def modify_site_and_house_dict_after_double(self, index, h_ind, h_ind1, site_id, sorted_site_keys, house_addresses):
        self.site_dict[site_id].num_houses = 1
        self.site_dict[sorted_site_keys[index]].num_houses = 1
        self.site_dict[site_id].house_address = [house_addresses[h_ind]]
        self.site_dict[sorted_site_keys[index]].house_address = [house_addresses[h_ind1]]
        self.site_dict[site_id].active = True
        self.site_dict[sorted_site_keys[index]].active = True
        self.house_dict[house_addresses[h_ind]].xt = self.site_dict[site_id].xt
        self.house_dict[house_addresses[h_ind]].yt = self.site_dict[site_id].yt
        self.house_dict[house_addresses[h_ind1]].xt = self.site_dict[sorted_site_keys[index]].xt + 1
        self.house_dict[house_addresses[h_ind1]].yt = self.site_dict[sorted_site_keys[index]].yt + 1
        self.house_dict[house_addresses[h_ind]].site = site_id
        self.house_dict[house_addresses[h_ind1]].site = sorted_site_keys[index]

    def fix_homeless_houses(self, sorted_site_keys):
        empty_sites = []
        for site_id in self.site_keys:
            if len(self.site_dict[site_id].house_address) == 0:
                empty_sites.append(site_id)

        for house_id in self.house_keys:
            if self.house_dict[house_id].site is None:

                house_num = int(house_id.split('_')[0])
                for e_site_id in empty_sites:
                    house_num1, house_num2 = None, None
                    e_index = sorted_site_keys.index(e_site_id)
                    e_index1 = e_index - 1
                    if e_index1 >= 0:
                        e_site_id1 = sorted_site_keys[e_index1]
                        house_id1 = self.site_dict[e_site_id1].house_address[0]
                        house_num1 = int(house_id1.split('_')[0])
                    e_index2 = e_index + 1
                    if e_index2 < len(sorted_site_keys):
                        e_site_id2 = sorted_site_keys[e_index2]
                        house_id2 = self.site_dict[e_site_id2].house_address[0]
                        house_num2 = int(house_id2.split('_')[0])

                    if house_num1 is not None and house_num2 is not None:
                        if house_num > house_num1 and house_num < house_num2:
                            self.site_dict[e_site_id].num_houses = 1
                            self.site_dict[e_site_id].house_address = [house_id]
                            self.site_dict[e_site_id].assigned = True
                            self.site_dict[e_site_id].active = True
                            self.house_dict[house_id].xt = self.site_dict[e_site_id].xt
                            self.house_dict[house_id].yt = self.site_dict[e_site_id].yt
                            self.house_dict[house_id].site = e_site_id

        # for site_id in self.site_keys:
        #     if not self.site_dict[site_id].active:
        #         del self.site_dict[site_id]
        #         sorted_site_keys.remove(site_id)
        # self.site_keys = list(self.site_dict.keys())
        return sorted_site_keys

    def sort_fixed_houses_and_sites_and_neighs(self, sorted_site_keys):

        house_numbers = []
        house_addresses = []
        for site_id in sorted_site_keys:
            if len(self.site_dict[site_id].house_address) > 0:
                house_addresses.append(self.site_dict[site_id].house_address[0])
                house_numbers.append(int(self.site_dict[site_id].house_address[0].split('_')[0]))
        house_numbers_sorted = np.argsort(house_numbers)
        house_addresses_sorted = [house_addresses[i] for i in house_numbers_sorted]

        new_site_dict = {}
        for i in range(len(house_addresses)):
            new_site_dict[i+1] = self.site_dict[sorted_site_keys[i]]
            new_site_dict[i + 1].address = [house_addresses[i]]

        new_house_dict = {}
        for i in range(len(house_addresses_sorted)):
            new_house_dict[house_addresses_sorted[i]] = self.house_dict[self.house_keys[i]]

        self.site_dict = new_site_dict
        self.house_dict = new_house_dict
        self.site_keys = list(self.site_dict.keys())
        self.house_keys = list(self.house_dict.keys())

        count = 0
        for house_id in house_addresses_sorted:
            count += 1
            self.house_dict[house_id].site = count
            self.house_dict[house_id].xt = self.site_dict[count].xt
            self.house_dict[house_id].yt = self.site_dict[count].yt
            self.site_dict[count].house_address = [house_id]

        for i in range(len(self.site_keys)):
            site_id = i+1
            neigh_sites = []
            if site_id > 1:
                neigh_sites.append(site_id-1)
            if site_id < len(self.site_keys):
                neigh_sites.append(site_id+1)
            self.site_dict[site_id].neigh_sites = neigh_sites

    def fix_site_duplicate(self):

        # Add on extra neigh sites that are not active to end of sites dictionary
        num_site_keys = len(self.site_keys)
        neigh_site_keys = list(self.neigh_site_dict.keys())

        for n_site_id in neigh_site_keys:
            self.neigh_site_dict[n_site_id].assigned = False
            area = abs(self.gt.find_area(self.neigh_site_dict[n_site_id].x_poly, self.neigh_site_dict[n_site_id].y_poly))
            _, self.neigh_site_dict[n_site_id].x_poly4, self.neigh_site_dict[n_site_id].y_poly4 = \
                self.gt.minimum_containing_paralleogram(self.neigh_site_dict[n_site_id].x_poly, self.neigh_site_dict[n_site_id].y_poly)
            area4 = abs(self.gt.find_area(self.neigh_site_dict[n_site_id].x_poly4, self.neigh_site_dict[n_site_id].y_poly4))
            if self.neigh_site_dict[n_site_id].active:
                if (self.get_min_distance_from_site_to_other_sites(n_site_id) < 0.1) and area > 150 and (abs(area-area4))/area4 < 0.2:
                    num_site_keys += 1
                    self.site_dict[num_site_keys] = self.neigh_site_dict[n_site_id]
            self.neigh_site_dict[n_site_id].active = False
        self.site_keys = list(self.site_dict.keys())

        # get sorted lists
        house_numbers, house_site_numbers, sort_index, sorted_site_keys = self.get_sorted_site_lists()
        # # got through sites and find doubles and move
        self.move_second_house_in_site_to_nearest_empty(sorted_site_keys)
        # # look for homeless houses
        sorted_site_keys = self.fix_homeless_houses(sorted_site_keys)
        # # sort fixed houses and sites and neighs
        self.sort_fixed_houses_and_sites_and_neighs(sorted_site_keys)

    def main_from_dash(self,house_address = None, tab_str = None, house_ID = None):

        self.house_dict = geo_locate_houses(house_address, self.house_dict)
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
        PostGIS_fns = Database()

        listOfSites = nearby_polygons(self.house_dict[house_ID].xd, self.house_dict[house_ID].yd, PostGIS_fns,
                                          0.0003)

        for count, geom in enumerate(listOfSites, start=0):
            if len(geom) > 1500:
                listOfSites.pop(count)

            gTwo, x_poly, y_poly = process_geometry(geom, self.gt)

            if len(x_poly) > 0:
                self.id += 1
                site_ob = SiteObject()
                site_ob.id = self.id
                site_ob.xt = sum(x_poly) / max(1, len(x_poly))
                site_ob.yt = sum(y_poly) / max(1, len(y_poly))
                site_ob.x_poly = x_poly
                site_ob.y_poly = y_poly
                site_ob.gTwo = gTwo
                aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(x_poly, y_poly)
                site_ob.aspect_ratio = aspect_ratio
                site_ob.orientation = orientation
                site_ob.area = abs(self.gt.find_area(x_poly, y_poly))
                site_ob.geom = geom
                site_ob.geom_27700 = PostGIS_fns.ST_Transform(geom)
                site_ob.num_houses = 1
                site_ob.neigh_sites = []
                site_ob.assigned = True
                self.site_dict[self.id] = site_ob
                self.site_dict[self.id].house_address.append(house_ID)
                self.house_dict[house_ID].site = self.id
                self.house_dict[house_ID].assigned = True

        return self.site_dict,self.house_dict

    def main(self, case, tab_str=None, house_address = None):
        if tab_str is None:
            tab_str = 'LynmouthDriveOdd'

        print('Getting house dict....')
        print('***', house_address, case)
        if case == 1:
            house_addresses = ['67 Lynmouth Dr Ruislip HA4 9BY UK', '51 Lynmouth Dr Ruislip HA4 9BY UK']
        elif case == 2:
            house_addresses = get_houses_os_walk()
        elif case == 3:
            house_addresses = spreadsheet_input(tab_str, self.excel_file_folder)
        elif case == 4 and house_address is not None:
            house_addresses = [house_address]
        print('***',house_addresses)

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
        PostGIS_fns = Database()

        for house_ID in self.house_dict.keys():
            print(house_ID)
            geom = take_from_database(self.house_dict[house_ID].xd, self.house_dict[house_ID].yd, PostGIS_fns)
            # neigh_geom_contact = find_neighs(geom, self.cur)
            neigh_geom_dist = nearby_polygons(self.house_dict[house_ID].xd, self.house_dict[house_ID].yd, PostGIS_fns, 0.0001)
            gTwo, x_poly, y_poly = process_geometry(geom, self.gt)
            dupeSiteFound_id = self.checkSitesForDupes(geom, self.site_dict)

            if dupeSiteFound_id != None:
                print('Duplicate Found for ID:', dupeSiteFound_id)
                self.site_dict[dupeSiteFound_id].num_houses += 1
                self.site_dict[dupeSiteFound_id].house_address.append(house_ID)
                self.site_dict[dupeSiteFound_id].assigned = True
                self.house_dict[house_ID].site = dupeSiteFound_id
                self.house_dict[house_ID].assigned = True
                for ng in neigh_geom_dist:
                    gTwo_ng, x_poly_ng, y_poly_ng = process_geometry(ng, self.gt)
                    aspect_ratio_ng, area_ng, orientation_ng = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                    if abs(orientation_ng - orientation) < 0.1 and area_ng > 35 and area_ng < 1000 and gTwo_ng != gTwo:
                        self.site_dict[dupeSiteFound_id].neigh_sites.append(gTwo_ng)
            elif len(x_poly) > 0:
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
                site_ob.area = abs(self.gt.find_area(x_poly, y_poly))
                site_ob.geom = geom
                site_ob.geom_27700 = PostGIS_fns.ST_Transform(geom)
                site_ob.num_houses = 1
                site_ob.neigh_sites = []
                site_ob.assigned = True
                self.site_dict[self.id] = site_ob
                self.site_dict[self.id].house_address.append(house_ID)
                self.house_dict[house_ID].site = self.id
                self.house_dict[house_ID].assigned = True
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
                    if len(x_poly_ng) > 0:
                        aspect_ratio_ng, area_ng, orientation_ng = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                        _, x_poly_ng4, y_poly_ng4 = self.gt.minimum_containing_paralleogram(x_poly_ng, y_poly_ng)
                        area_ng4 = abs(self.gt.find_area(x_poly_ng4, y_poly_ng4))
                        if abs(orientation_ng - orientation) < 0.1 and area_ng > 100 and area_ng < 1000 and abs(area_ng - area_ng4)/area_ng4 < 0.2:
                            self.neigh_id += 1
                            n_site_ob = SiteObject()
                            n_site_ob.id = self.neigh_id
                            n_site_ob.xt = sum(x_poly_ng)/max(1, len(x_poly_ng))
                            n_site_ob.yt = sum(y_poly_ng)/max(1, len(y_poly_ng))
                            n_site_ob.x_poly = x_poly_ng
                            n_site_ob.y_poly = y_poly_ng
                            n_site_ob.gTwo = gTwo_ng
                            n_site_ob.geom = ng
                            n_site_ob.geom_27700 = PostGIS_fns.ST_Transform(ng)
                            aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(x_poly_ng, y_poly_ng)
                            n_site_ob.aspect_ratio = aspect_ratio
                            n_site_ob.orientation = orientation
                            n_site_ob.area = abs(self.gt.find_area(x_poly_ng, y_poly_ng))
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
                if ng_dupeSiteFound_id_1 == None:
                    ng_gtwo_list_temp.append(ng)
                    neigh_sites_id.append(ng_dupeSiteFound_id_2)
            # self.site_dict[k].neigh_sites = [list(x) for x in set(tuple(x) for x in ng_gtwo_list_temp)]
            self.site_dict[k].neigh_sites = list(set(neigh_sites_id))

        self.fix_site_duplicate()
        self.plotter(tab_str)

    def main_from_pickle(self, tab_str):
        with open(self.pickle_file_folder + tab_str + '.pickle', 'rb') as f:
            loadedDict = pickle.load(f)
        self.site_dict = loadedDict['site_dict']
        self.neigh_site_dict = loadedDict['neigh_site_dict']
        self.house_dict = loadedDict['house_dict']
        self.site_keys = list(self.site_dict.keys())
        self.house_keys = list(self.house_dict.keys())

        # self.plotter(tab_str)
        self.fix_site_duplicate()
        self.plotter(tab_str)

    def save_to_pickle(self, tab_str):
        dict = {
            'house_dict': self.house_dict,
            'site_dict': self.site_dict,
            'neigh_site_dict': self.neigh_site_dict
        }
        with open(self.pickle_file_folder + tab_str + '.pickle', 'wb') as f:
            pickle.dump(dict, f)


if __name__ == '__main__':
    start = time.time()

    # Choose street for processing
    wb = openpyxl.load_workbook('/Users/andrewbashorm/Dropbox/auto_processing/excel_files/house_lists.xlsx')
    pickle_file_list = list(wb.sheetnames)
    pickle_file = pickle_file_list[5]

    load_from_pickle = True
    sf = SiteFinder(pickle_file_folder, excel_file_folder)
    # pickle_file = pickle_file_folder[0]
    # if load_from_pickle:
    #     sf.main_from_pickle(pickle_file)
    # else:
    #     sf.main(3, pickle_file)
    g,b,c = '67 Lynmouth Drive Ruislip HA4 9BY', 'LynmouthDriveOdd', '67_HA4_9BY'
    ff, gg = sf.main_from_dash(g,b,c)
    # sf.save_to_pickle(pickle_file)

    end = time.time()
    keys = sf.house_dict.keys()

    print('Time Taken:', round(end - start), 'seconds')

