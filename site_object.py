
import numpy as np

class SiteObject(object):
    def __init__(self):
        self.id = None
        self.house_address_list = None
        self.x = None
        self.y = None
        self.x_poly = []
        self.y_poly = []
        self.geom = None
        # self.org_geom = None
        self.geom_27700 = None
        self.multi_house = None
        self.area = None
        self.neigh_sites = []

    def main(self):
        pass