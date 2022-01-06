import numpy as np
import os
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pickle
from geometry import Geometry

class FixData(object):
    def __init__(self):
        self.gt = Geometry()
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))

    def load_from_pickle(self, pickle_file):
        with open(pickle_file, 'rb') as f:
            loadedDict = pickle.load(f)
        self.site_dict = loadedDict['site_dict']
        self.neigh_site_dict = loadedDict['neigh_site_dict']
        self.house_dict = loadedDict['house_dict']
        self.site_keys = list(self.site_dict.keys())
        self.house_keys = list(self.house_dict.keys())
        self.pickle_file = os.path.basename(pickle_file).split('2')[0]
        print(self.pickle_file)

    def save_to_pickle(self, pickle_file):
        dict = {
            'house_dict': self.house_dict,
            'site_dict': self.site_dict,
            'neigh_site_dict': self.neigh_site_dict
        }
        with open(pickle_file, 'wb') as f:
            pickle.dump(dict, f)

    def fix_house_address(self):
        for site_id in self.site_keys:
            house_id = self.site_dict[site_id].house_address
            if type(house_id) is str:
                self.site_dict[site_id].house_address = [house_id]

    def create_box_around_polygons(self):
        for site_id in self.site_keys:
            _, self.site_dict[site_id].x_poly4, self.site_dict[site_id].y_poly4 = \
                self.gt.minimum_containing_paralleogram(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly)
            house_id = self.site_dict[site_id].house_address[0]
            _, self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4 = \
                self.gt.minimum_containing_paralleogram(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)

    def make_plot(self):
        plt.figure(figsize=(15, 10))
        # Make plot
        # for i in self.house_keys:
        #     text = i.split('_')[0]
        #     plt.text(self.house_dict[i].xt, self.house_dict[i].yt, text)
        max_x, min_x = -100000, 100000
        max_y, min_y = -100000, 100000
        for site_id in self.site_keys:
            site_centre = plt.plot(self.site_dict[site_id].xt, self.site_dict[site_id].yt, '.', color='r', label='Site Centre')
            plt.fill(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly, fill=False, color='b')
            plt.fill(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly, fill=True, color='lightblue')
            if max(self.site_dict[site_id].x_poly)> max_x:
                max_x = max(self.site_dict[site_id].x_poly)
                min_x = min(self.site_dict[site_id].x_poly)
                max_y = max(self.site_dict[site_id].y_poly)
                min_y = min(self.site_dict[site_id].y_poly)

        for site_id in self.site_keys:
            # plt.fill(self.site_dict[site_id].x_poly4, self.site_dict[site_id].y_poly4, color='c', fill=False, linewidth=1)
            site_front = plt.plot([self.site_dict[site_id].x_poly4[0], self.site_dict[site_id].x_poly4[1]], [self.site_dict[site_id].y_poly4[0],self.site_dict[site_id].y_poly4[1]], '-', color='r', linewidth=2, label='Site Front')
            house_id = self.site_dict[site_id].house_address[0]
            house_centre = plt.plot(self.house_dict[house_id].xt, self.house_dict[house_id].yt, '.', color='g', label='House Centre')
            plt.fill(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds, color='g', fill=False, linewidth=1)
            # plt.fill(self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4, color='orange', fill=False, linewidth=2)
            house_front = plt.plot([self.house_dict[house_id].X_bounds4[0], self.house_dict[house_id].X_bounds4[1]], [self.house_dict[house_id].Y_bounds4[0], self.house_dict[house_id].Y_bounds4[1]], '-', color='orange', linewidth=2, label='House Front')
            xb = 0.5*(self.site_dict[site_id].x_poly4[2] + self.site_dict[site_id].x_poly4[3])
            yb = 0.5*(self.site_dict[site_id].y_poly4[2] + self.site_dict[site_id].y_poly4[3])
            # plt.quiver(xb, yb, np.cos(self.site_dict[site_id].orientation), np.sin(self.site_dict[site_id].orientation), scale=0.00000000000001)
            for i in range(len(self.site_dict[site_id].X_extra)):
                other_buildings = plt.fill(self.site_dict[site_id].X_extra[i], self.site_dict[site_id].Y_extra[i], ':', color='darkred', fill=False, linewidth=1)

            plt.xlim(min_x-10, max_x+10)
            plt.ylim(min_y-10, max_y+10)
            plt.legend([site_centre[0], site_front[0], house_centre[0], house_front[0]],
                       ['Site Centre', 'Site Front', 'House Centre', 'House Front'])
            plt.title('Geolocation after correction (' + self.pickle_file + ')')
            plt.ticklabel_format(axis='both', style='sci')
            plt.xlabel('Longitude (EPSG:27700)')
            plt.ylabel('Latitude (EPSG:27700)')
            plt.axis('equal')
            plt.show()

    def plot_single_house(self, site_id):
        house_id = self.site_dict[site_id].house_address[0]
        plt.fill(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly, color='b', linewidth=1, fill=False)
        plt.fill(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds, color='g', fill=False, linewidth=1)
        # print(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)
        _, x, y = self.gt.minimum_containing_paralleogram(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)
        plt.fill(x, y, color='orange', fill=False, linewidth=2)

    def fix_centres(self):
        for k in self.site_keys:
            xt = sum(self.site_dict[k].x_poly4)/len(self.site_dict[k].x_poly4)
            yt = sum(self.site_dict[k].y_poly4)/len(self.site_dict[k].y_poly4)
            self.site_dict[k].xt = xt
            self.site_dict[k].yt = yt
            house_id = self.site_dict[k].house_address[0]
            xt = sum(self.house_dict[house_id].X_bounds4)/len(self.house_dict[house_id].X_bounds4)
            yt = sum(self.house_dict[house_id].Y_bounds4)/len(self.house_dict[house_id].Y_bounds4)
            self.house_dict[house_id].xt = xt
            self.house_dict[house_id].yt = yt

    def find_back_and_front_of_polygon(self):

        for k in self.site_keys:
            # get data out of dictionaries
            orientation = self.site_dict[k].orientation
            xs, ys = self.site_dict[k].x_poly4, self.site_dict[k].y_poly4
            house_id = self.site_dict[k].house_address[0]
            xh, yh = self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4
            cxh, cyh = sum(xh)/len(xh), sum(yh)/len(yh)
            inds = []

            # get front and back edge of minimum poly
            for i in range(len(xs)):
                i1 = (i+1)%len(xs)
                u = [xs[i1] - xs[i], ys[i1] - ys[i]]
                l = np.sqrt(u[0]**2 + u[1]**2)
                u = [u[0]/l, u[1]/l]
                v = [np.cos(orientation), np.sin(orientation)]
                if abs(np.dot(u, v)) < 0.5:
                    inds.append(i)

            # find front of site polygon
            front_id, min_dist = -1, 10000
            for i in inds:
                i1 = (i + 1) % len(xs)
                mx, my = 0.5*(xs[i] + xs[i1]), 0.5*(ys[i] + ys[i1])
                dist = np.sqrt((cxh - mx)**2 + (cyh - my)**2)
                if dist < min_dist:
                    min_dist = dist
                    front_id = i
            # sort minimum poly
            xs = self.gt.shift_list(xs, front_id)
            ys = self.gt.shift_list(ys, front_id)
            self.site_dict[k].x_poly4 = xs
            self.site_dict[k].y_poly4 = ys

            # find front of house polygon
            front_id, min_dist = -1, 10000
            fx, fy = 0.5 * (xs[0] + xs[1]), 0.5 * (ys[0] + ys[1])
            for i in range(len(xh)):
                i1 = (i+1)%len(xh)
                mx, my = 0.5 * (xh[i] + xh[i1]), 0.5 * (yh[i] + yh[i1])
                dist = np.sqrt((fx - mx) ** 2 + (fy - my) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    front_id = i

            # sort minimum poly
            xh = self.gt.shift_list(xh, front_id)
            yh = self.gt.shift_list(yh, front_id)
            self.house_dict[house_id].X_bounds4 = xh
            self.house_dict[house_id].Y_bounds4 = yh

    def correct_site_orientation(self):
        for k in self.site_keys:
            # get data out of dictionaries
            xs, ys = self.site_dict[k].x_poly4, self.site_dict[k].y_poly4
            aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(xs, ys)
            u = [xs[2] - xs[1], ys[2] - ys[1]]
            l = np.sqrt(u[0] ** 2 + u[1] ** 2)
            u = [u[0] / l, u[1] / l]
            orientation = np.arctan2(u[1],u[0])
            # if np.dot(u, [np.cos(orientation), np.sin(orientation)]) < 0:
            #     orientation = (orientation + np.pi)%2*np.pi
            self.site_dict[k].orientation = orientation

    def get_house_orientation(self):
            for k in self.house_keys:
                # get data out of dictionaries
                xs, ys = self.house_dict[k].X_bounds4, self.house_dict[k].Y_bounds4
                aspect_ratio, area, orientation = self.gt.get_aspect_ratio_area(xs, ys)
                u = [xs[2] - xs[1], ys[2] - ys[1]]
                l = np.sqrt(u[0] ** 2 + u[1] ** 2)
                u = [u[0] / l, u[1] / l]
                orientation = np.arctan2(u[1], u[0])
                # if np.dot(u, [np.cos(orientation), np.sin(orientation)]) < 0:
                #     orientation = (orientation + np.pi)%2*np.pi
                self.house_dict[k].orientation = orientation

    def side_distances(self):
        for k in self.site_keys:
            # get data out of dictionaries
            xs, ys = self.site_dict[k].x_poly4, self.site_dict[k].y_poly4
            house_id = self.site_dict[k].house_address[0]
            xh, yh = self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4
            p0, p1, p2, p3 = [xs[0], ys[0]], [xs[1], ys[1]], [xs[2], ys[2]], [xs[3], ys[3]]
            q0, q1, q2, q3 = [xh[0], yh[0]], [xh[1], yh[1]], [xh[2], yh[2]], [xh[3], yh[3]]
            self.house_dict[house_id].left_distance = min(self.gt.distance(q0, q3, p0), self.gt.distance(q0, q3, p3))
            self.house_dict[house_id].right_distance = min(self.gt.distance(q1, q2, p1), self.gt.distance(q1, q2, p2))

    def fix_site_and_house_neighs(self):

        # go through sites and find closest neighbour
        for site_id1 in self.site_keys:
            d = []
            ids = []
            xt1, yt1 = self.site_dict[site_id1].xt, self.site_dict[site_id1].yt
            for site_id2 in self.site_keys:
                xt2, yt2 = self.site_dict[site_id2].xt, self.site_dict[site_id2].yt
                d.append(np.sqrt((xt1 - xt2)**2 + (yt1 - yt2)**2))
                ids.append(site_id2)
            d_sorted = sorted(d, key=float)
            n1 = ids[d.index(d_sorted[1])]
            n2 = ids[d.index(d_sorted[2])]
            xtn1, ytn1 = self.site_dict[n1].xt, self.site_dict[n1].yt
            xtn2, ytn2 = self.site_dict[n2].xt, self.site_dict[n2].yt
            d_12 = np.sqrt((xtn1 - xtn2)**2 + (ytn1 - ytn2)**2)

            if d_12 < d_sorted[1]:
                site_neighs = [n1]
            elif d_12 < d_sorted[2]:
                site_neighs = [n2]
            else:
                site_neighs = [n1, n2]

            # sort neighs left to right
            if len(site_neighs) == 2:
                xp0, yp0 = self.site_dict[site_id1].x_poly4, self.site_dict[site_id1].y_poly4
                xp1, yp1 = self.site_dict[site_neighs[0]].x_poly4, self.site_dict[site_neighs[0]].y_poly4
                xp2, yp2 = self.site_dict[site_neighs[1]].x_poly4, self.site_dict[site_neighs[1]].y_poly4
                u0 = [xp0[1] - xp0[0], yp0[1] - yp0[0]]
                mx0, my0 = 0.5*(xp0[1] + xp0[0]), 0.5*(yp0[1] + yp0[0])
                mx1, my1 = 0.5*(xp1[1] + xp1[0]), 0.5*(yp1[1] + yp1[0])
                mx2, my2 = 0.5*(xp2[1] + xp2[0]), 0.5*(yp2[1] + yp2[0])
                u1 = [mx0 - mx1, my0 - my1]
                u2 = [mx0 - mx2, my0 - my2]
                if np.dot(u0, u1) < 0:
                    site_neighs.reverse()
            elif len(site_neighs) == 1:
                xp0, yp0 = self.site_dict[site_id1].x_poly4, self.site_dict[site_id1].y_poly4
                xp1, yp1 = self.site_dict[site_neighs[0]].x_poly4, self.site_dict[site_neighs[0]].y_poly4
                u0 = [xp0[1] - xp0[0], yp0[1] - yp0[0]]
                mx0, my0 = 0.5 * (xp0[1] + xp0[0]), 0.5 * (yp0[1] + yp0[0])
                mx1, my1 = 0.5 * (xp1[1] + xp1[0]), 0.5 * (yp1[1] + yp1[0])
                u1 = [mx0 - mx1, my0 - my1]
                if np.dot(u0, u1) < 0:
                    site_neighs = [None] + site_neighs
                else:
                    site_neighs = site_neighs + [None]

            self.site_dict[site_id1].neigh_sites_id = site_neighs

            # get house neighs
            house_id = self.site_dict[site_id1].house_address[0]
            house_neighs = []
            for neigh_site_id in site_neighs:
                if neigh_site_id is not None:
                    house_neighs.append(self.site_dict[neigh_site_id].house_address[0])
                else:
                    house_neighs.append(None)
            # print(site_neighs, house_neighs)
            self.house_dict[house_id].neigh_house_id = house_neighs


    def main(self, pickle_file, pickle_file_folder):
        self.load_from_pickle(pickle_file_folder + pickle_file + '.pickle')
        self.fix_house_address()
        self.create_box_around_polygons()
        self.fix_centres()
        self.find_back_and_front_of_polygon()
        self.correct_site_orientation()
        self.get_house_orientation()
        self.side_distances()
        self.fix_site_and_house_neighs()

        self.make_plot()
        # self.save_to_pickle(pickle_file_folder + pickle_file + '.pickle')

if __name__ == '__main__':

    fd = FixData()
    pickle_file_name = 'site_finder_lynmouth_odd1'
    fd.main(pickle_file_name)

    # # load all sites and houses from pickle
    # pickle_file_name = 'site_finder_lynmouth_odd1'
    # fd.load_from_pickle(pickle_file_name + '.pickle')
    # fd.fix_house_address()
    # fd.create_box_around_polygons()
    # fd.fix_centres()
    # fd.find_back_and_front_of_polygon()
    # fd.correct_site_orientation()
    # fd.side_distances()
    #
    # fd.make_plot()
    # pickle_file_name = 'site_finder_lynmouth_odd2'
    # fd.save_to_pickle(pickle_file_name + '.pickle')


    # fd.plot_single_house(6)
