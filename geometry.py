# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
import numpy as np
from numpy import linalg as LA

import json
import pickle
import os
from os import path
from pathlib import Path
import matplotlib.pyplot as plt
import sys
import math
import random
from pathlib import Path
import constants
from pyproj import Proj, transform

class Geometry(object):
    def __init__(self):
        pass

    def convert_lat_lon_to_27700(self, lat, lon):
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:27700')
        return transform(inProj, outProj, lat, lon)

    def convert_27700_to_lat_lon(self, x1, y1):
        inProj = Proj(init='epsg:27700')
        outProj = Proj(init='epsg:4326')
        return transform(inProj, outProj, x1, y1)

    def convert_list_lat_lon_to_27700(self, lat_list, lon_list):
        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:27700')
        X, Y = [], []
        for p in range(len(lat_list)):
            x_temp, y_temp = transform(inProj, outProj, lat_list[p], lon_list[p])
            X.append(x_temp)
            Y.append(y_temp)
        return X, Y

    def convert_list_27700_to_lat_lon(self, X_list, Y_list):
        inProj = Proj(init='epsg:27700')
        outProj = Proj(init='epsg:4326')
        lat_list, lon_list = [], []
        for p in range(len(X_list)):
            lat_temp, lon_temp = transform(inProj, outProj, X_list[p], Y_list[p])
            lat_list.append(lat_temp)
            lon_list.append(lon_temp)
        return lat_list, lon_list

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

    def main(self):
        x = [0, 20, 20, 0]
        y = [0, 0, 100, 100]
        print(self.get_aspect_ratio_area(x, y))

if __name__ == '__main__':
    gt = Geometry()
    gt.main()