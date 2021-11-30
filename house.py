
import numpy as np

class House(object):
    def __init__(self):
        self.id = None
        self.address = None
        self.postcode = None
        self.house_number = None
        self.xd = None
        self.yd = None
        self.xt = None
        self.yt = None
        self.point = None
        self.point_t = None
        self.location = None
        self.sites = None
        self.neigh_site = None
        self.potential_neighs = None
        self.pts = []
        self.vectors = []
        self.ptsf = []
        self.vectorsf = []
        self.ground_height = None
        self.cluster_centre_x = None
        self.cluster_centre_y = None
        self.vector_img_link = ''
        self.raster_img_link = ''

    def main(self):
        pass