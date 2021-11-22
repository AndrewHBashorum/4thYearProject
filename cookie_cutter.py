import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

from geometry import Geometry

class CookieCutter(object):
    def __init__(self, HOUSES=[]):
        self.HOUSES = HOUSES
        self.gt = Geometry()

    def get_height_data(self, plot_bool):
        for i in range(len(self.HOUSES)):
            x, y = self.HOUSES[i]['x_poly'], self.HOUSES[i]['y_poly']
            X_, Y_, Z_, faces, pts, normals, ptsf, normalsf = self.gt.basic_model_from_height_data(x, y, plot_bool, self.HOUSES[i]['address_name'])
            x_, y_, zl_, zu_ = np.array(pts[0]), np.array(pts[1]), np.array(pts[2]), np.array(pts[3])
            u_, v_, w_ = np.array(normals[0]), np.array(normals[1]), np.array(normals[2])
            xf_, yf_, zf_ = np.array(ptsf[0]), np.array(ptsf[1]), np.array(ptsf[2])
            uf_, vf_, wf_ = np.array(normalsf[0]), np.array(normalsf[1]), np.array(normalsf[2])

            l_ = np.sqrt(np.multiply(u_, u_) + np.multiply(v_, v_) + np.multiply(w_, w_))
            lf_ = np.sqrt(np.multiply(uf_, uf_) + np.multiply(vf_, vf_) + np.multiply(wf_, wf_))
            p_ = l_ > 0.0
            pf_ = lf_ > 0.0
            x_  = [x_[k] for k, j in enumerate(p_) if j]
            y_  = [y_[k] for k, j in enumerate(p_) if j]
            zl_ = [zl_[k] for k, j in enumerate(p_) if j]
            zu_ = [zu_[k] for k, j in enumerate(p_) if j]
            u_  = [u_[k] for k, j in enumerate(p_) if j]
            v_  = [v_[k] for k, j in enumerate(p_) if j]
            w_  = [w_[k] for k, j in enumerate(p_) if j]
            xf_ = [xf_[k] for k, j in enumerate(pf_) if j]
            yf_ = [yf_[k] for k, j in enumerate(pf_) if j]
            zf_ = [zf_[k] for k, j in enumerate(pf_) if j]
            uf_ = [uf_[k] for k, j in enumerate(pf_) if j]
            vf_ = [vf_[k] for k, j in enumerate(pf_) if j]
            wf_ = [wf_[k] for k, j in enumerate(pf_) if j]

            # PTS = np.column_stack((x_ + xf_, y_ + yf_))
            # kmeans = KMeans(n_clusters=2)
            # kmeans.fit(PTS)
            # y_kmeans = kmeans.predict(PTS)
            #
            # plt.scatter(PTS[:, 0], PTS[:, 1], c=y_kmeans, s=50, cmap='viridis')
            # centers = kmeans.cluster_centers_
            # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);

            plt.fill(x,   y,   fill=False, color='b')
            plt.plot(x_,  y_,  '.', color='r')
            plt.plot(xf_, yf_, '.', color='g')

        return


