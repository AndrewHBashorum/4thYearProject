import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

from geometry import Geometry
import random
class CookieCutter(object):
    def __init__(self, HOUSES=[]):
        self.HOUSES = HOUSES
        self.gt = Geometry()

    def get_height_data(self, plot_bool):
        for i in self.site_id_list:
            x, y = self.site_dict[i].x_poly, self.site_dict[i].y_poly
            pts, normals, ptsf, normalsf = self.gt.basic_model_from_height_data(x, y, plot_bool)
            x_, y_, zl_, zu_ = np.array(pts[0]), np.array(pts[1]), np.array(pts[2]), np.array(pts[3])
            u_, v_, w_ = np.array(normals[0]), np.array(normals[1]), np.array(normals[2])
            xf_, yf_, zf_ = np.array(ptsf[0]), np.array(ptsf[1]), np.array(ptsf[2])
            uf_, vf_, wf_ = np.array(normalsf[0]), np.array(normalsf[1]), np.array(normalsf[2])

            l_ = np.sqrt(np.multiply(u_, u_) + np.multiply(v_, v_) + np.multiply(w_, w_))
            lf_ = np.sqrt(np.multiply(uf_, uf_) + np.multiply(vf_, vf_) + np.multiply(wf_, wf_))
            p_ = l_ > 0.0
            pf_ = lf_ > 0.0

            x_ = [x_[k] for k, j in enumerate(p_) if j]
            y_ = [y_[k] for k, j in enumerate(p_) if j]
            zl_ = [zl_[k] for k, j in enumerate(p_) if j]
            zu_ = [zu_[k] for k, j in enumerate(p_) if j]
            u_ = [u_[k] for k, j in enumerate(p_) if j]
            v_ = [v_[k] for k, j in enumerate(p_) if j]
            w_ = [w_[k] for k, j in enumerate(p_) if j]
            xf_ = [xf_[k] for k, j in enumerate(pf_) if j]
            yf_ = [yf_[k] for k, j in enumerate(pf_) if j]
            zf_ = [zf_[k] for k, j in enumerate(pf_) if j]
            uf_ = [uf_[k] for k, j in enumerate(pf_) if j]
            vf_ = [vf_[k] for k, j in enumerate(pf_) if j]
            wf_ = [wf_[k] for k, j in enumerate(pf_) if j]

            PTS = np.column_stack((x_ + xf_, y_ + yf_))
            kmeans = KMeans(n_clusters=2)
            kmeans.fit(PTS)
            y_kmeans = kmeans.predict(PTS)

            plt.scatter(PTS[:, 0], PTS[:, 1], c=y_kmeans, s=10, cmap='viridis')
            centers = kmeans.cluster_centers_
            plt.scatter(centers[:, 0], centers[:, 1], c='black', s=20, alpha=0.5);

            # plt.fill(x,   y,   fill=False, color='b')
            plt.plot(x_, y_, '.', color='r')
            plt.plot(xf_, yf_, '.', color='g')

        return

    def open_pickle(self):

        with open('site_finder_all.pickle', 'rb') as f:
            self.loadedDict = pickle.load(f)

    def singleStreetSide(self, streetSide):

        self.site_dict = self.loadedDict[streetSide]['site_dict']
        self.neigh_site_dict = self.loadedDict[streetSide]['neigh_site_dict']
        self.house_dict = self.loadedDict[streetSide]['house_dict']

        self.site_id_list = self.site_dict.keys()

        pass

    def singleHouse(self, streetSide, house):

        self.site_dict = self.loadedDict[streetSide]['site_dict']
        self.site_id_list = self.loadedDict[streetSide]['house_dict'][house].sites

        pass




if __name__ == '__main__':

    street = 'lynmouthOdd'
    house = '53_HA4_9BY'

    cc = CookieCutter()
    cc.open_pickle()
    cc.singleHouse(street,house)
    cc.get_height_data(False)








# with open('site_finder_lynmouth_odd.pickle', 'rb') as f:
#     loadedDict = pickle.load(f)
#
# with open('lynEven.pickle', 'rb') as f:
#     loadedDictLE = pickle.load(f)
#
# with open('site_finder_BemptonDrive_odd.pickle', 'rb') as f:
#     loadedDictDO = pickle.load(f)
#
# with open('site_finder_BemptonDrive_even.pickle', 'rb') as f:
#     loadedDictDE = pickle.load(f)
#
# with open('BeverleyRoadOdd.pickle', 'rb') as f:
#     loadedDictDRO = pickle.load(f)
#
# with open('BeverleyRoadEven.pickle', 'rb') as f:
#     loadedDictDRE = pickle.load(f)
#
# dict = {
#     'lynmouthOdd': loadedDict,
#     'lynmouthEven': loadedDictLE,
#     'BemptonDriveOdd': loadedDictDO,
#     'BemptonDriveEven': loadedDictDE,
#     'BeverleyRoadOdd': loadedDictDRO,
#     'BeverleyRoadEven': loadedDictDRE
# }
#
# with open('site_finder_all.pickle', 'wb') as handle:
#     pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)