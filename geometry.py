# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
import numpy as np
from numpy import linalg as LA

import json
import pickle5 as pickle
import os
from os import path
from pathlib import Path
import matplotlib.pyplot as plt
import sys
import math
import random
from pathlib import Path
import constants

class Geometry(object):
    def __init__(self):
        pass

    def centre_poly(self, x, y):
        cx = sum(x) / max(1, len(x))
        cy = sum(y) / max(1, len(y))

        return cx, cy

    def poly_angles(self, x, y, cx, cy):
        cx = sum(x) / max(1, len(x))
        cy = sum(y) / max(1, len(y))
        return [np.fmod(np.arctan2((y[i] - cy), (x[i] - cx)) + 2 * np.pi, 2 * np.pi) for i in range(len(x))]

    def flip_array(self, x, y):
        x_temp = []
        y_temp = []
        for i in range(len(x)):
            x_temp.append(x[len(x) - (i + 1)])
            y_temp.append(y[len(x) - (i + 1)])
        x = x_temp
        y = y_temp
        return x, y

    def sort_array_acw(self, x, y):
        cx, cy = self.centre_poly(x, y)
        angle = self.poly_angles(x, y, cx, cy)

        cw_acw = 0
        for i in range(len(x)):
            j = (i + 1) % len(x)
            if (angle[j] - angle[i] > 0):
                cw_acw += 1
            else:
                cw_acw -= 1
        if (cw_acw < 0):
            x, y = self.flip_array(x, y)

        return x, y

    def find_area(self, x, y):
        cx = sum(x)/max(len(x), 1)
        cy = sum(y)/max(len(y), 1)
        area = 0
        for i in range(len(x)):
            j = (i + 1) % len(x)
            area += 0.5 * ((x[i] - cx) * (y[j] - cy) - (x[j] - cx) * (y[i] - cy))
        return area

    def get_aspect_ratio_area(self, x, y):
        M = np.zeros((2, 2))
        cx = sum(x) / max(len(x), 1)
        cy = sum(y) / max(len(y), 1)
        area = 0
        for i in range(len(x)):
            i1 = (i + 1) % len(x)
            area += 0.5 * abs((x[i1] - cx) * (y[i] - cy) - (x[i] - cx) * (y[i1] - cy))
            ix = x[i] - cx
            iy = y[i] - cy
            M[0][0] += ix ** 2
            M[1][1] += iy ** 2
            M[0][1] -= ix * iy
            M[1][0] -= ix * iy
        eig = LA.eig(M)[0]
        evec = LA.eig(M)[1]
        if eig[0] > eig[1]:
            v = evec[0]
        else:
            v = evec[1]
        orientation = np.arctan2(v[1], v[0])%np.pi
        evalues = [eig[0].real, eig[1].real]
        evalues = [abs(i) for i in evalues]
        aspect_ratio = np.sqrt(max(evalues) / min(evalues))
        area = round(100 * area) / 100

        return aspect_ratio, area, orientation

    def point_in_polygon(self, px, py, x, y):
        # returns True if point (px, py) is in polygon (x, y) and False otherwise
        x0, y0 = x[:], y[:]
        c = False
        n = len(x0)
        for i in range(n):
            j = (i - 1) % len(x0)
            if (((y0[i] > py) != (y0[j] > py)) and (
                    px >= ((x0[j] - x0[i]) * (py - y0[i]) / (y0[j] - y0[i])) + x0[i])):
                c = not c
        return c

    def get_pts_normals_elevations(self, x, y):

        Pts = []
        Normals = []
        Ele = []

        with open('../tileSections/Tile_bounds.pickle', 'rb') as f:
            Tile = pickle.load(f)

        tile_ind = []
        for i in range(len(x)):
            for count, tile in enumerate(Tile):
                x_tile, y_tile = tile[0], tile[1]
                if self.point_in_polygon(x[i], y[i], x_tile, y_tile):
                    tile_ind.append(count)
        tile_ind = list(set(tile_ind))

        for tile in tile_ind:

            with open('../tileSections/Tile_-20_7_section_pts_' + str(tile) + '.pickle','rb') as f:
                temp_pts = pickle.load(f)

            with open('../tileSections/Tile_-20_7_section_normals_' + str(tile) + '.pickle','rb') as f:
                temp_normals = pickle.load(f)

            with open('../tileSections/Tile_-20_7_section_ele_' + str(tile) + '.pickle','rb') as f:
                temp_ele = pickle.load(f)

            for i in range(len(temp_pts)):
                p = temp_pts[i]
                e = temp_ele[i]
                n = temp_normals[i]
                l = np.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
                if self.point_in_polygon(p[0],p[1], x, y) and l > 0.1:
                    Ele.append(e)
                    Pts.append(p)
                    Normals.append(n)

            # with open('../tileSections/Tile_-20_7_section_pts_' + str(tile) + '.txt') as f:
            #     temp_pts = f.readlines()
            #     temp_pts = ast.literal_eval(temp_pts[0])
            #     Pts = Pts + temp_pts
            # with open('../tileSections/Tile_-20_7_section_normals_' + str(tile) + '.txt') as f:
            #     temp_normals = f.readlines()
            #     temp_normals = ast.literal_eval(temp_normals[0])
            #     Normals = Normals + temp_normals[0]
            # with open('../tileSections/Tile_-20_7_section_ele_' + str(tile) + '.txt') as f:
            #     temp_ele = f.readlines()
            #     temp_ele = ast.literal_eval(temp_ele[0])
            #     Ele = Ele + temp_ele

        return Pts, Normals, Ele


    def find_centre(self, x, y):

        g = 0
        for i in x:
            g = g + x
        centreX = g / len(x)

        for i in y:
            f = f + x
        centreY = f / len(x)

        centre = [centreX,centreY]
        return centre


    def split_pts_vertical_and_rest(self, Pts, Ele, Normals, trim):

        # Points and normals of house
        x_, y_, zl_, zu_, u_, v_, w_ = [], [], [], [], [], [], []
        # Points and normals of flat parts
        xf_, yf_, zf_, uf_, vf_, wf_ = [], [], [], [], [], []

        for i1 in range(int(len(Pts) / trim)):
            i = trim * i1
            px = Pts[i][0]
            py = Pts[i][1]

            if (Normals[i][1]) < 0.9:
                x_.append(Pts[i][0])
                y_.append(Pts[i][1])
                zl_.append(Ele[i])
                zu_.append(Ele[i] + Pts[i][2])
                if Normals[i][1] > 0:
                    u_.append(Normals[i][0])
                    v_.append(Normals[i][1])
                    w_.append(Normals[i][2])
                else:
                    u_.append(-Normals[i][0])
                    v_.append(-Normals[i][1])
                    w_.append(-Normals[i][2])
            else:
                xf_.append(Pts[i][0])
                yf_.append(Pts[i][1])
                zf_.append(Ele[i] + Pts[i][2])
                uf_.append(Normals[i][0])
                vf_.append(Normals[i][1])
                wf_.append(Normals[i][2])

        return x_, y_, zl_, zu_, u_, v_, w_, xf_, yf_, zf_, uf_, vf_, wf_

    def plot_normals_and_colour_map(self, pts, normals, ptsf, normalsf, house_name=''):

        x_, y_, zl_, zu_ = pts[0], pts[1], pts[2], pts[3]
        u_, v_, w_ = normals[0], normals[1], normals[2]
        xf_, yf_, zf_ = ptsf[0], ptsf[1], ptsf[2]
        uf_, vf_, wf_ = normalsf[0], normalsf[1], normalsf[2]
        if len(uf_) > 0:
            max_u, min_u = max(max(u_), max(uf_)), min(min(u_), min(uf_))
            max_v, min_v = max(max(v_), max(vf_)), min(min(v_), min(vf_))
            max_w, min_w = max(max(w_), max(wf_)), min(min(w_), min(wf_))
        elif len(u_) > 0:
            max_u, min_u = max(u_), min(u_)
            max_v, min_v = max(v_), min(v_)
            max_w, min_w = max(w_), min(w_)

        print('*', len(x_))
        fig = plt.figure()
        plt.axis("off")
        for i in range(len(x_)):
            col = [(u_[i] - min_u) / (max_u - min_u), (v_[i] - min_v) / (max_v - min_v),
                   (w_[i] - min_w) / (max_w - min_w)]
            plt.scatter(x_[i], y_[i], s=50, color=col)  # s=marker_size,
        for i in range(len(xf_)):
            col = [(uf_[i] - min_u) / (max_u - min_u), (vf_[i] - min_v) / (max_v - min_v),
                   (wf_[i] - min_w) / (max_w - min_w)]
            plt.scatter(xf_[i], yf_[i], s=50, color=col)
        plt.show()
        plt.savefig('images/vector_images/' + house_name + ".png", format='png', bbox_inches='tight', dpi=300)
        # if len(house_name) > 0:
        #     plt.savefig('images/vector_images/'+house_name+ ".png", format='png', bbox_inches='tight', dpi=300)
        #     # plt.savefig(png_file, format='png', bbox_inches='tight', dpi=300)
        #     temp_dict = {'x_': x_, 'y_': y_, 'zl_': zl_, 'zu_': zu_, 'u_': u_, 'v_': v_, 'w_': w_, 'xf_': xf_,
        #                  'yf_': yf_, 'zf_': zf_, 'uf_': uf_, 'vf_': vf_, 'wf_': wf_, }
        #     save_data = house_name + '_data.pickle'
        #     with open(save_data, 'wb') as handle:
        #         pickle.dump(temp_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

        dx, dy, dz = max(x_) - min(x_), max(y_) - min(y_), max(zu_) - min(zu_)
        d = max(dx, dy, dz)
        delta = 2
        mx, my, mz = 0.5 * (max(x_) + min(x_)), 0.5 * (max(y_) + min(y_)), 0.5 * (max(zu_) + min(zu_))

        #fig = plt.figure()


    def basic_model_from_height_data(self, x, y, plot_bool,house_key):

        Pts, Normals, Ele = self.get_pts_normals_elevations(x, y)
        trim = 1
        # marker_size = 50
        x_, y_, zl_, zu_, u_, v_, w_, xf_, yf_, zf_, uf_, vf_, wf_ = self.split_pts_vertical_and_rest(Pts, Ele, Normals, trim)
        pts = [x_, y_, zl_, zu_]
        # center = self.find_centre(x_,y_)
        normals = [u_, v_, w_]
        ptsf = [xf_, yf_, zf_]
        normalsf = [uf_, vf_, wf_]

        if plot_bool:
            self.plot_normals_and_colour_map(pts, normals, ptsf, normalsf,house_key)

        # Test v different roof shapes
        #fig = plt.figure()

        # if plot_bool:
        #     fig = plt.figure()
        # roof_shape, roof_ridge = self.default_roof_shapes(x, y)
        # roof_ind = self.simple_alignment_cor_fun(roof_shape, roof_ridge, x_, y_, u_, v_, w_, plot_bool)

        # # Test v different roof shapes
        # X_, Y_, Z_, faces = self.plot_basic_house(x, y, x_, y_, zl_, zu_, roof_shape, roof_ridge, roof_ind, plot_bool)

        return pts, normals, ptsf, normalsf

    def main(self):
        x = [0, 20, 20, 0]
        y = [0, 0, 100, 100]
        print(self.get_aspect_ratio_area(x, y))

if __name__ == '__main__':

    gt = Geometry()
    gt.main()