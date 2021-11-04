
class SiteObject(object):
    def __init__(self):
        self.id = None
        self.house_address_list = []
        self.xt = None
        self.yt = None
        self.x_poly = []
        self.y_poly = []
        self.geom = None
        # self.org_geom = None
        self.geom_27700 = None
        self.multi_house = False
        self.area = None
        self.neigh_sites = []
        self.neigh_sites_id = []
        self.aspect_ratio = None
        self.orientation = None

    def main(self):
        pass