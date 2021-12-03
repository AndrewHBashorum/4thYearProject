import pickle
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import requests
from io import BytesIO
from PIL import Image
from geometry import Geometry
import time
class CookieCutter(object):
    def __init__(self, HOUSES=[]):
        self.HOUSES = HOUSES
        self.gt = Geometry()

    def get_height_data(self, plot_bool):
        for i in self.site_id_list:
            x, y = self.site_dict[i].x_poly, self.site_dict[i].y_poly
            pts, normals, ptsf, normalsf = self.gt.basic_model_from_height_data(x, y, plot_bool,self.site_dict[i].house_address_list[0])
            x_, y_, zl_, zu_ = np.array(pts[0]), np.array(pts[1]), np.array(pts[2]), np.array(pts[3])
            u_, v_, w_ = np.array(normals[0]), np.array(normals[1]), np.array(normals[2])
            xf_, yf_, zf_ = np.array(ptsf[0]), np.array(ptsf[1]), np.array(ptsf[2])
            uf_, vf_, wf_ = np.array(normalsf[0]), np.array(normalsf[1]), np.array(normalsf[2])

            self.save_vector_pickle(i,pts, normals, ptsf, normalsf)

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


            # plt.scatter(PTS[:, 0], PTS[:, 1], c=y_kmeans, s=10, cmap='viridis')
            # centers = kmeans.cluster_centers_
            # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=20, alpha=0.5);
            #
            # # plt.fill(x,   y,   fill=False, color='b')
            # plt.plot(x_, y_, '.', color='r')
            # plt.plot(xf_, yf_, '.', color='g')

        return

    def open_pickle(self):

        with open('house_site_pickle/site_finder_all.pickle', 'rb') as f:
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

    def combinePickleFiles(self):
        directory = 'house_site_pickle/'
        with open(directory + 'lynmouthDriveOdd.pickle', 'rb') as f:
            loadedDict = pickle.load(f)

        with open(directory + 'lynmouthDriveEven.pickle', 'rb') as f:
            self.loadedDictLE = pickle.load(f)

        with open(directory + 'BemptonDriveOdd.pickle', 'rb') as f:
            loadedDictDO = pickle.load(f)

        with open(directory + 'BemptonDriveEven.pickle', 'rb') as f:
            loadedDictDE = pickle.load(f)

        with open(directory + 'BeverleyRoadOdd.pickle', 'rb') as f:
            loadedDictDRO = pickle.load(f)

        with open(directory + 'BeverleyRoadEven.pickle', 'rb') as f:
            loadedDictDRE = pickle.load(f)

        dict = {
            'lynmouthDriveOdd': loadedDict,
            'lynmouthDriveEven': self.loadedDictLE,
            'BemptonDriveOdd': loadedDictDO,
            'BemptonDriveEven': loadedDictDE,
            'BeverleyRoadOdd': loadedDictDRO,
            'BeverleyRoadEven': loadedDictDRE
        }

        with open(directory + 'site_finder_all.pickle', 'wb') as handle:
            pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def find_raster_Image(self,house_key, center = ['51.567703','0.403389']):

        newString = requests.get('https://maps.googleapis.com/maps/api/staticmap?center=' + center[0] + ',%20-' + center[1] + '&zoom=20&size=200x200&maptype=satellite&format=png&scale=2&key=AIzaSyAcQIYA9e_qvw7MBLBzqLXMe4m8VIN2agY')
        img = Image.open(BytesIO(newString.content))
        img.save('images/raster_images/' + house_key, format ='PNG')

    def save_vector_pickle(self, i, pts, normals, ptsf, normalsf):

        temp_dict = {'pts': pts, 'normals':normals, 'ptsf':ptsf, 'normalsf':normalsf}
        save_data = self.site_dict[i].house_address_list[0] + '_data.pickle'
        with open(save_data, 'wb') as handle:
            pickle.dump(temp_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    start = time.perf_counter()
    #
    # street = 'lynmouthDriveOdd'
    # house = '53_HA4_9BY'
    #
    cc = CookieCutter()
    #cc.findImage()
    cc.combinePickleFiles()
    #cc.open_pickle()
    #cc.singleStreetSide(street)
    # print(cc.house_dict['1_HA4_9BY'])
    #cc.singleHouse(street,house)
    #cc.get_height_data(True)

    end = time.perf_counter()
    print(f"Finished in {(start - end) / 60 :0.4f} minutes")










