import numpy as np
import os
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


    def save_to_pickle(self, pickle_file):
        dict = {
            'house_dict': self.house_dict,
            'site_dict': self.site_dict,
            'neigh_site_dict': self.neigh_site_dict
        }
        with open(pickle_file, 'wb') as f:
            pickle.dump(dict, f)

    def fix_house_address_list(self):
        for site_id in self.site_keys:
            house_id = self.site_dict[site_id].house_address_list
            if type(house_id) is str:
                self.site_dict[site_id].house_address_list = [house_id]

    def create_box_around_polygons(self):
        for site_id in self.site_keys:
            _, self.site_dict[site_id].x_poly4, self.site_dict[site_id].y_poly4 = \
                self.gt.minimum_containing_paralleogram(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly)
            house_id = self.site_dict[site_id].house_address_list[0]
            _, self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4 = \
                self.gt.minimum_containing_paralleogram(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)

    def make_plot(self):
        plt.figure()
        # Make plot
        for site_id in self.site_keys:
            plt.plot(self.site_dict[site_id].xt, self.site_dict[site_id].yt, 'o', color='b')
            plt.fill(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly, color='b', linewidth=1, fill=False)
            plt.fill(self.site_dict[site_id].x_poly4, self.site_dict[site_id].y_poly4, color='c', fill=False, linewidth=1)
            plt.plot([self.site_dict[site_id].x_poly4[0], self.site_dict[site_id].x_poly4[1]], [self.site_dict[site_id].y_poly4[0],self.site_dict[site_id].y_poly4[1]], '-', color='r', linewidth=2)
            house_id = self.site_dict[site_id].house_address_list[0]
            plt.plot(self.house_dict[house_id].xt, self.house_dict[house_id].yt, 'o', color='g')
            plt.fill(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds, color='g', fill=False, linewidth=1)
            plt.fill(self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4, color='orange', fill=False, linewidth=2)
            plt.plot([self.house_dict[house_id].X_bounds4[0], self.house_dict[house_id].X_bounds4[1]], [self.house_dict[house_id].Y_bounds4[0],self.house_dict[house_id].Y_bounds4[1]], '-', color='r', linewidth=2)
            xb = 0.5*(self.site_dict[site_id].x_poly4[2] + self.site_dict[site_id].x_poly4[3])
            yb = 0.5*(self.site_dict[site_id].y_poly4[2] + self.site_dict[site_id].y_poly4[3])
            # plt.quiver(xb, yb, np.cos(self.site_dict[site_id].orientation), np.sin(self.site_dict[site_id].orientation), scale=0.00000000000001)
            for i in range(len(self.site_dict[site_id].X_extra)):
                plt.fill(self.site_dict[site_id].X_extra[i], self.site_dict[site_id].Y_extra[i], color='darkred', fill=False, linewidth=2)

    def plot_single_house(self, site_id):
        house_id = self.site_dict[site_id].house_address_list[0]
        plt.fill(self.site_dict[site_id].x_poly, self.site_dict[site_id].y_poly, color='b', linewidth=1, fill=False)
        plt.fill(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds, color='g', fill=False, linewidth=1)
        print(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)
        _, x, y = self.gt.minimum_containing_paralleogram(self.house_dict[house_id].X_bounds, self.house_dict[house_id].Y_bounds)
        plt.fill(x, y, color='orange', fill=False, linewidth=2)

    def fix_centres(self):
        for k in self.site_keys:
            xt = sum(self.site_dict[k].x_poly4)/len(self.site_dict[k].x_poly4)
            yt = sum(self.site_dict[k].y_poly4)/len(self.site_dict[k].y_poly4)
            self.site_dict[k].xt = xt
            self.site_dict[k].yt = yt
            house_id = self.site_dict[k].house_address_list[0]
            xt = sum(self.house_dict[house_id].X_bounds4)/len(self.house_dict[house_id].X_bounds4)
            yt = sum(self.house_dict[house_id].Y_bounds4)/len(self.house_dict[house_id].Y_bounds4)
            self.house_dict[house_id].xt = xt
            self.house_dict[house_id].yt = yt

    def find_back_and_front_of_polygon(self):

        for k in self.site_keys:
            # get data out of dictionaries
            orientation = self.site_dict[k].orientation
            xs, ys = self.site_dict[k].x_poly4, self.site_dict[k].y_poly4
            house_id = self.site_dict[k].house_address_list[0]
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
            house_id = self.site_dict[k].house_address_list[0]
            xh, yh = self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4
            p0, p1, p2, p3 = [xs[0], ys[0]], [xs[1], ys[1]], [xs[2], ys[2]], [xs[3], ys[3]]
            q0, q1, q2, q3 = [xh[0], yh[0]], [xh[1], yh[1]], [xh[2], yh[2]], [xh[3], yh[3]]
            self.house_dict[house_id].left_distance = min(self.gt.distance(q0, q3, p0), self.gt.distance(q0, q3, p3))
            self.house_dict[house_id].right_distance = min(self.gt.distance(q1, q2, p1), self.gt.distance(q1, q2, p2))

    def main(self, pickle_file_name):
        self.load_from_pickle(pickle_file_name + '.pickle')
        self.fix_house_address_list()
        self.create_box_around_polygons()
        self.fix_centres()
        self.find_back_and_front_of_polygon()
        self.correct_site_orientation()
        self.get_house_orientation()
        self.side_distances()

        self.make_plot()
        pickle_file_name = 'site_finder_lynmouth_odd2'
        self.save_to_pickle(pickle_file_name + '.pickle')

if __name__ == '__main__':

    fd = FixData()
    pickle_file_name = 'site_finder_lynmouth_odd1'
    fd.main(pickle_file_name)

    # # load all sites and houses from pickle
    # pickle_file_name = 'site_finder_lynmouth_odd1'
    # fd.load_from_pickle(pickle_file_name + '.pickle')
    # fd.fix_house_address_list()
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
