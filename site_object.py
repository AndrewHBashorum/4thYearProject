
class SiteObject(object):
    def __init__(self):
        self.house_address = []
        self.leftSite = False
        self.mainSite = False
        self.rightSite = False
        self.selected = False
        self.xt = None
        self.yt = None
        self.gTwo = []
        self.x_poly = []
        self.y_poly = []
        self.x_poly4 = []
        self.y_poly4 = []
        self.geom = None
        self.geom_27700 = None
        self.num_houses = False
        self.neigh_sites = []
        self.area = None
        self.aspect_ratio = None
        self.orientation = None
        self.active = True
        self.assigned = False
        self.X_main = []
        self.Y_main = []
        self.X_extra = []
        self.Y_extra = []

    def main(self):
        pass