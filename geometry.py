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
        evalues = [eig[0].real, eig[1].real]
        evalues = [abs(i) for i in evalues]
        aspect_ratio = np.sqrt(max(evalues) / min(evalues))
        area = round(100 * area) / 100

        return aspect_ratio, area