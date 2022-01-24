
import numpy as np

class House(object):
    def __init__(self):
        self.address = None
        self.postcode = None
        self.house_number = None
        self.xd = None
        self.yd = None
        self.xt = None
        self.yt = None
        self.location = None
        self.site = None
        self.potential_neighs = None
        self.pts = []
        self.vectors = []
        self.ptsf = []
        self.vectorsf = []
        self.ground_height = None
        self.cluster_centre_x = None
        self.cluster_centre_y = None
        self.img_link = ''
        self.X_bounds = []
        self.Y_bounds = []
        self.X_bounds4 = []
        self.Y_bounds4 = []
        self.assigned = False

    def main(self):
        pass