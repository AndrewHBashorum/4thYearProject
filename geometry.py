# Author: ANDREW BASHORUM: C00238900
# 4th YEAR PROJECT
import numpy as np
from numpy import linalg as LA
from scipy.spatial import ConvexHull

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


    def rotate_polygon(self, x, y, alpha):

        x_ = x[:]
        y_ = y[:]
        cx, cy = sum(x) / len(x), sum(y) / len(y)
        for i in range(len(x)):
            x[i] = ((x_[i] - cx) * np.cos(alpha) - (y_[i] - cy) * np.sin(alpha)) + cx
            y[i] = ((x_[i] - cx) * np.sin(alpha) + (y_[i] - cy) * np.cos(alpha)) + cy
        return x, y

    def enlarge_polygon(self, x, y, scale_factor):

        cx, cy = sum(x) / len(x), sum(y) / len(y)
        x_temp, y_temp = [], []
        for i in range(len(x)):
            x_temp.append(scale_factor*(x[i] - cx) + cx)
            y_temp.append(scale_factor*(y[i] - cy) + cy)

        return x_temp, y_temp

    def polygon_in_enlarged_polygon(self, qx, qy, x, y, scale_factor):
        x_temp, y_temp = self.enlarge_polygon(x, y, scale_factor)
        poly_in_poly = True
        for i in range(len(qx)):
            if not self.point_in_polygon(qx[i], qy[i], x_temp, y_temp):
                poly_in_poly = False
        return poly_in_poly

    def antipodal_pairs(self, x0, y0):
        l = []
        n = len(x0)
        p1 = [x0[0], y0[0]]
        p2 = [x0[1], y0[1]]

        t, d_max = None, 0
        for p in range(1, n):
            pn = [x0[p], y0[p]]
            d = self.distance(p1, p2, pn)
            if d > d_max:
                t, d_max = p, d
        l.append(t)

        for p in range(1, n):
            p1 = [x0[p % n], y0[p % n]]
            p2 = [x0[(p + 1) % n], y0[(p + 1) % n]]
            _p = [x0[t % n], y0[t % n]]
            _pp = [x0[(t + 1) % n], y0[(t + 1) % n]]

            while self.distance(p1, p2, _pp) > self.distance(p1, p2, _p):
                t = (t + 1) % n
                _p = [x0[t % n], y0[t % n]]
                _pp = [x0[(t + 1) % n], y0[(t + 1) % n]]
            l.append(t)

        return l

    def parallel_vector(self, a, b, c):
        v0 = [c[0] - a[0], c[1] - a[1]]
        v1 = [b[0] - c[0], b[1] - c[1]]
        return [c[0] - v0[0] - v1[0], c[1] - v0[1] - v1[1]]

    def line_intersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # finds intersection between lines, given 2 points on each line.
        # (x1, y1), (x2, y2) on 1st line, (x3, y3), (x4, y4) on 2nd line.
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        return px, py

    def compute_parallelogram(self, x, y, l, z1, z2, n):
        # from each antipodal point, draw a parallel vector,
        # so ap1->ap2 is parallel to p1->p2
        #    aq1->aq2 is parallel to q1->q2
        p1 = [x[z1 % n], y[z1 % n]]
        p2 = [x[(z1 + 1) % n], y[(z1 + 1) % n]]
        q1 = [x[z2 % n], y[z2 % n]]
        q2 = [x[(z2 + 1) % n], y[(z2 + 1) % n]]
        ap1 = [x[l[z1 % n]], y[l[z1 % n]]]
        aq1 = [x[l[z2 % n]], y[l[z2 % n]]]
        ap2, aq2 = self.parallel_vector(p1, p2, ap1), self.parallel_vector(q1, q2, aq1)

        a = self.line_intersection(p1[0], p1[1], p2[0], p2[1], q1[0], q1[1], q2[0], q2[1])
        b = self.line_intersection(p1[0], p1[1], p2[0], p2[1], aq1[0], aq1[1], aq2[0], aq2[1])
        d = self.line_intersection(ap1[0], ap1[1], ap2[0], ap2[1], q1[0], q1[1], q2[0], q2[1])
        c = self.line_intersection(ap1[0], ap1[1], ap2[0], ap2[1], aq1[0], aq1[1], aq2[0], aq2[1])

        s = self.distance(a, b, c) * math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

        return s, a, b, c, d

    def distance(self, p1, p2, p):
        denom = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
        if denom > 0.0:
            return abs(((p2[1] - p1[1]) * p[0] - (p2[0] - p1[0]) * p[1] + p2[0] * p1[1] - p2[1] * p1[0]) / denom)
        else:
            return 0

    def minimum_containing_paralleogram(self, x, y):
        # returns score, area, points from top-left, clockwise , favouring low area

        z1, z2 = 0, 0
        n = len(x)
        points = np.zeros((n, 2))
        for i in range(n):
            points[i, 0] = x[i]
            points[i, 1] = y[i]
        hull = ConvexHull(points)
        xh = []
        yh = []

        for i in hull.vertices:
            xh.append(hull.points[i][0])
            yh.append(hull.points[i][1])

        # for each edge, find antipodal vertice for it (step 1 in paper).
        l = self.antipodal_pairs(xh, yh)
        n = len(xh)
        so, ao, bo, co, do, z1o, z2o = 100000000000, None, None, None, None, None, None

        # step 2 in paper.
        for z1 in range(n):
            if z1 >= z2:
                z2 = z1 + 1
            p1 = [xh[z1 % n], yh[z1 % n]]
            p2 = [xh[(z1 + 1) % n], yh[(z1 + 1) % n]]
            a = [xh[z2 % n], yh[z2 % n]]
            b = [xh[(z2 + 1) % n], yh[(z2 + 1) % n]]
            c = [xh[l[z2 % n]], yh[l[z2 % n]]]

            if self.distance(p1, p2, a) >= self.distance(p1, p2, b):
                continue

            while self.distance(p1, p2, c) > self.distance(p1, p2, b):
                z2 += 1
                a = [xh[z2 % n], yh[z2 % n]]
                b = [xh[(z2 + 1) % n], yh[(z2 + 1) % n]]
                c = [xh[l[z2 % n]], yh[l[z2 % n]]]

            st, at, bt, ct, dt = self.compute_parallelogram(xh, yh, l, z1, z2, n)
            xt = [at[0], bt[0], ct[0], dt[0]]
            yt = [at[1], bt[1], ct[1], dt[1]]
            inside = 1
            for i in range(n):
                ans = self.point_in_polygon(xh[i], yh[i], xt, yt)
                if (ans < 0):
                    inside = 0
            if (st < so) and (inside == 1):
                so, ao, bo, co, do, z1o, z2o = st, at, bt, ct, dt, z1, z2
        x1 = [ao[0], bo[0], co[0], do[0]]
        y1 = [ao[1], bo[1], co[1], do[1]]
        x1, y1 = self.sort_array_acw(x1, y1)

        return 1, x1, y1

    def shift_list(self, seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]

    def shift_polygon(self, x, y, dx, dy):
        for i in range(len(x)):
            x[i] += dx
            y[i] += dy
        return x, y

    def main(self):
        x = [0, 20, 20, 0]
        y = [0, 0, 100, 100]
        print(self.get_aspect_ratio_area(x, y))

if __name__ == '__main__':
    gt = Geometry()
    gt.main()