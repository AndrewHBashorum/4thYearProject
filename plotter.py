

import matplotlib.pyplot as plt
import pickle

class Plotter(object):

    def __init__(self):
        self.open_pickle()
        pass

    def plotSites(self, neigh_site_id_list, neigh_site_dict, site_id_list, site_dict):
        plt.figure()

        for i in neigh_site_id_list:
            if neigh_site_dict[i].active:
                plt.fill(neigh_site_dict[i].x_poly, neigh_site_dict[i].y_poly, ':', fill=False, color='r', linewidth=3)

        for i in site_id_list:
            plt.fill(site_dict[i].x_poly, site_dict[i].y_poly, fill=False, color='b')


    def open_pickle(self):


        # with open('house_site_pickle/site_finder_all.pickle', 'rb') as f:
        #     self.loadedDict = pickle.load(f)
        with open('/Users/andrewbashorm/Dropbox/auto_processing/pickle_files/BeverleyRoadEven4.pickle', 'rb') as f:
            self.loadedDict = pickle.load(f)


    def singleStreetSide2(self, streetSide):
        self.site_dict = self.loadedDict[streetSide]['site_dict']
        self.neigh_site_dict = self.loadedDict[streetSide]['neigh_site_dict']
        self.house_dict = self.loadedDict[streetSide]['house_dict']

        self.site_id_list = self.site_dict.keys()
        self.neigh_site_id_list = self.neigh_site_dict.keys()

        self.plotSites(self.neigh_site_id_list,self.neigh_site_dict,self.site_id_list,self.site_dict)

    def singleStreetSide(self):
        self.site_dict = self.loadedDict['site_dict']
        self.neigh_site_dict = self.loadedDict['neigh_site_dict']
        self.house_dict = self.loadedDict['house_dict']

        self.site_id_list = self.site_dict.keys()
        self.neigh_site_id_list = self.neigh_site_dict.keys()

        self.plotSites(self.neigh_site_id_list,self.neigh_site_dict,self.site_id_list,self.site_dict)


    def singleHouse(self, streetSide, house):
        self.site_dict = self.loadedDict[streetSide]['site_dict']

        self.site_id_list = self.loadedDict[streetSide]['house_dict'][house].sites
        self.neigh_site_dict = self.loadedDict[streetSide]['neigh_site_dict']

        self.neigh_site_id_list = self.site_dict[self.site_id_list[0]].neigh_sites_id

        self.plotSites(self.neigh_site_id_list,self.neigh_site_dict,self.site_id_list,self.site_dict)

    def plot_normals_and_colour_map(self, pts, normals, ptsf, normalsf, house_name=''):

        x_, y_, zl_, zu_ = pts[0], pts[1], pts[2], pts[3]
        u_, v_, w_ = normals[0], normals[1], normals[2]
        xf_, yf_, zf_ = ptsf[0], ptsf[1], ptsf[2]
        uf_, vf_, wf_ = normalsf[0], normalsf[1], normalsf[2]
        if len(uf_) > 0:
            max_u, min_u = max(max(u_), max(uf_)), min(min(u_), min(uf_))
            max_v, min_v = max(max(v_), max(vf_)), min(min(v_), min(vf_))
            max_w, min_w = max(max(w_), max(wf_)), min(min(w_), min(wf_))
        elif len(u_) > 0:
            max_u, min_u = max(u_), min(u_)
            max_v, min_v = max(v_), min(v_)
            max_w, min_w = max(w_), min(w_)

        print('*', len(x_))
        fig = plt.figure()
        plt.axis("off")
        for i in range(len(x_)):
            col = [(u_[i] - min_u) / (max_u - min_u), (v_[i] - min_v) / (max_v - min_v),
                   (w_[i] - min_w) / (max_w - min_w)]
            plt.scatter(x_[i], y_[i], s=50, color=col)  # s=marker_size,
        for i in range(len(xf_)):
            col = [(uf_[i] - min_u) / (max_u - min_u), (vf_[i] - min_v) / (max_v - min_v),
                   (wf_[i] - min_w) / (max_w - min_w)]
            plt.scatter(xf_[i], yf_[i], s=50, color=col)
        plt.show()
        plt.savefig('images/vector_images/' + house_name + ".png", format='png', bbox_inches='tight', dpi=300)

    def basic_model_from_height_data(self, x, y, plot_bool, house_name=''):

        temp_dict = {'x': x, 'y': y}
        if len(house_name) > 0:
            save_data = house_name + '_position.pickle'

            with open(save_data, 'wb') as handle:
                pickle.dump(temp_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


        # Move pts and normals into z,y,z arrays and split vertical groups

        Pts, Normals, Ele = self.get_pts_normals_elevations(x, y)
        trim = 1
        # marker_size = 50
        x_, y_, zl_, zu_, u_, v_, w_, xf_, yf_, zf_, uf_, vf_, wf_ = self.split_pts_vertical_and_rest(Pts, Ele, Normals,
                                                                                                      trim)
        pts = [x_, y_, zl_, zu_]
        normals = [u_, v_, w_]
        ptsf = [xf_, yf_, zf_]
        normalsf = [uf_, vf_, wf_]
        if plot_bool:
            self.plot_normals_and_colour_map(pts, normals, ptsf, normalsf)

        # Test v different roof shapes
        if plot_bool:
            fig = plt.figure()
        roof_shape, roof_ridge = self.default_roof_shapes(x, y)
        roof_ind = self.simple_alignment_cor_fun(roof_shape, roof_ridge, x_, y_, u_, v_, w_, plot_bool)

        # Test v different roof shapes
        X_, Y_, Z_, faces = self.plot_basic_house(x, y, x_, y_, zl_, zu_, roof_shape, roof_ridge, roof_ind, plot_bool)

        return X_, Y_, Z_, faces, pts, normals, ptsf, normalsf

    def entire(self):

        self.neigh_site_dict_list = []
        self.site_dict_list = []
        self.house_dict_list = []
        self.site_id_list = []
        self.neigh_site_id_list = []

        for i in self.loadedDict.keys():
            self.site_dict_list.append(self.loadedDict[i]['site_dict'])
            self.neigh_site_dict_list.append(self.loadedDict[i]['neigh_site_dict'])
            self.house_dict_list.append(self.loadedDict[i]['house_dict'])
            self.site_id_list.append(self.loadedDict[i]['site_dict'].keys())
            self.neigh_site_id_list.append(self.loadedDict[i]['neigh_site_dict'].keys())

        count = 0
        for i in self.neigh_site_id_list:
            for e in i:
                plt.fill(self.neigh_site_dict_list[count][e].x_poly, self.neigh_site_dict_list[count][e].y_poly, ':', fill=False, color='r',
                             linewidth=3)
            count +=1

        count = 0

        for i in self.site_id_list:
            for e in i:
                plt.fill(self.site_dict_list[count][e].x_poly, self.site_dict_list[count][e].y_poly, ':', fill=False, color='b',
                             linewidth=3)
            count +=1



if __name__ == '__main__':

    street = 'lynmouthDriveEven'
    house = '52_HA4_9BY'
    #house = '53_HA4_9BY'

    plotter = Plotter()
    plotter.singleStreetSide()
    # plotter.singleHouse(street,house)
    # plotter.entire()
