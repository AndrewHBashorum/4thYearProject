

import matplotlib.pyplot as plt
import pickle
import os
from mpl_toolkits.mplot3d import Axes3D


class Plotter(object):

    def __init__(self):

        pass

    def plotSites(self, neigh_site_id_list, neigh_site_dict, site_id_list, site_dict):
        plt.figure()

        for i in neigh_site_id_list:
            if i != None and i != '':
                if neigh_site_dict[i].active:
                    plt.fill(neigh_site_dict[i].x_poly, neigh_site_dict[i].y_poly, ':', fill=False, color='r', linewidth=3)

        if type(site_id_list) == list:
            for i in site_id_list:
                if i != None and i != '':
                    plt.fill(site_dict[i].x_poly, site_dict[i].y_poly, fill=False, color='b')
        else:
            i = site_id_list
            if i != None and i != '':
                plt.fill(site_dict[i].x_poly, site_dict[i].y_poly, fill=False, color='b')

    def plotSitesWithHouse(self, site_id_list, site_dict,house_dict):
        plt.figure()
        # Make plot
        self.tolerance = 50

        if type(site_id_list) == list:
            for i in site_id_list:

                xt = house_dict[site_dict[i].address[0]].xt
                yt = house_dict[site_dict[i].address[0]].yt

                plt.plot(xt, yt, 'x')
                plt.fill(site_dict[i].x_poly, site_dict[i].y_poly, color='b', linewidth=2, fill=False)
                # plt.fill([xt - self.tolerance, xt + self.tolerance ,xt + self.tolerance, xt - self.tolerance],
                #          [yt - self.tolerance, yt - self.tolerance, xt + self.tolerance, yt + self.tolerance], color='orange', fill=False)
                plt.fill(site_dict[i].X_main, site_dict[i].Y_main, color='lightgreen', linewidth=1)
        else:
            i = site_id_list
            xt = house_dict[site_dict[i].address[0]].xt
            yt = house_dict[site_dict[i].address[0]].yt

            plt.plot(xt, yt, 'x')
            plt.fill(site_dict[i].x_poly, site_dict[i].y_poly, color='b', linewidth=2, fill=False)
            # plt.fill([xt - self.tolerance, xt + self.tolerance ,xt + self.tolerance, xt - self.tolerance],
            #          [yt - self.tolerance, yt - self.tolerance, xt + self.tolerance, yt + self.tolerance], color='orange', fill=False)
            plt.fill(site_dict[i].X_main, site_dict[i].Y_main, color='lightgreen', linewidth=1)


    def open_house_pickle(self, street):

        print('well')
        with open('/Users/andrewbashorm/Dropbox/auto_processing/pickle_files/' +street+'4.pickle', 'rb') as f:
            self.loadedDict = pickle.load(f)


    def singleStreetSide(self):

        self.site_dict = self.loadedDict['site_dict']
        self.neigh_site_dict = self.loadedDict['neigh_site_dict']
        self.house_dict = self.loadedDict['house_dict']

        self.site_id_list = list(self.site_dict.keys())
        self.neigh_site_id_list = self.neigh_site_dict.keys()




    def singleHouse(self, house):
        self.site_dict = self.loadedDict['site_dict']
        self.house_dict = self.loadedDict['house_dict']
        self.site_id_list = self.loadedDict['house_dict'][house].site
        self.neigh_site_dict = self.loadedDict['neigh_site_dict']

        if type(self.site_id_list) == list:
            self.neigh_site_id_list = self.site_dict[self.site_id_list[0]].neigh_sites_id
        else:
            self.neigh_site_id_list = self.site_dict[self.site_id_list].neigh_sites_id


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

    def quiver(self):

        pts = self.loadedHeightDict['pts']
        normals = self.loadedHeightDict['normals']
        ptsf = self.loadedHeightDict['ptsf']
        normalsf = self.loadedHeightDict['normalsf']

        x_, y_, zl_, zu_ = pts[0], pts[1], pts[2], pts[3]
        u_, v_, w_ = normals[0], normals[1], normals[2]
        xf_, yf_, zf_ = ptsf[0], ptsf[1], ptsf[2]
        uf_, vf_, wf_ = normalsf[0], normalsf[1], normalsf[2]

        dx, dy, dz = max(x_) - min(x_), max(y_) - min(y_), max(zu_) - min(zu_)
        d = max(dx, dy, dz)
        delta = 2
        mx, my, mz = 0.5 * (max(x_) + min(x_)), 0.5 * (max(y_) + min(y_)), 0.5 * (max(zu_) + min(zu_))

        fig = plt.figure()

        ax1 = Axes3D(fig)
        ax1.view_init(elev=30., azim=-174.)
        ax1.set_xlim3d(mx - d / 2, mx + d / 2)
        ax1.set_ylim3d(my - d / 2, my + d / 2)
        ax1.set_zlim3d(mz - d / 2 - delta, mz + d / 2 - delta)
        ax1.axis("off")
        ax1.quiver(x_, y_, zu_, u_, w_, v_, length=1, color='b')
        ax1.plot(x_, y_, zl_, '.', color='r')

    def entire(self):

        self.neigh_site_dict_list = []
        self.site_dict_list = []
        self.house_dict_list = []
        self.site_id_list = []
        self.neigh_site_id_list = []
        streetKeys = ['BemptonDriveOdd', 'LynmouthDriveEven','LynmouthDriveOdd','BemptonDriveEven','BeverleyRoadOddA','BeverleyRoadOddB','BeverleyRoadEven']
        for i in streetKeys:
            self.open_house_pickle(i)
            self.site_dict_list.append(self.loadedDict['site_dict'])
            self.neigh_site_dict_list.append(self.loadedDict['neigh_site_dict'])
            self.house_dict_list.append(self.loadedDict['house_dict'])
            self.site_id_list.append(self.loadedDict['site_dict'].keys())
            self.neigh_site_id_list.append(self.loadedDict['neigh_site_dict'].keys())

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

    def open_height_pickle(self,street, house):

        with open('/Users/andrewbashorm/Dropbox/auto_processing/pickle_files/' +street+'_height/height_data_' + house + '.pickle', 'rb') as f:
            self.loadedHeightDict = pickle.load(f)

        pass

    def clearConsole(self):
        lambda: print('\n' * 150)

    def getStreet(self,streetchoice,sideChoice):

        streetchoice = int(streetchoice)
        sideChoice = int(sideChoice)

        if streetchoice == 1:
            street = 'LynmouthDrive'
        if streetchoice == 2:
            street = 'BemptonDrive'
        if streetchoice == 3:
            street = 'BeverleyRoad'

        if sideChoice == 1:
            side = 'Odd'
        if sideChoice == 2:
            side = 'Even'

        street = street + side

        return street

if __name__ == '__main__':

    plotter = Plotter()
    outputChoice = 0
    def choices():

        outputChoice = input('Enter which output is needed: 1= Single House , 2= Single Street, 3= Entire List, 4 = Quit')

        if outputChoice != '4':
            if outputChoice == '3':
                plotter.entire()
            else:
                streetchoice = input('Choose your street: 1 = Lynmouth Drive, 2 = Bempton, 3= Beverley ')
                sideChoice = input('Choose your street: 1 = Odd, 2 = Even ')
                street = plotter.getStreet(streetchoice, sideChoice)
                if outputChoice == '1':
                    house = input('Enter house key: ')
                    plotter.open_house_pickle(street)
                    plotter.open_height_pickle(street, house)

                    plotter.singleHouse(house)
                    plotter.quiver()

                if outputChoice == '2':
                    plotter.open_house_pickle(street)

                    plotter.singleStreetSide()

                plotter.plotSites(plotter.neigh_site_id_list, plotter.neigh_site_dict, plotter.site_id_list,
                                  plotter.site_dict)
                plotter.plotSitesWithHouse(plotter.site_id_list, plotter.site_dict, plotter.house_dict)
        return outputChoice

    while outputChoice != '4':
        outputChoice = choices()
        plotter.clearConsole()






    street = 'BemptonDriveOdd'
    house = '63_HA4_9DB'
    #house = '53_HA4_9BY'




    #plotter.singleStreetSide()
    #plotter.singleHouse(house)
    # plotter.make_plot_single_site_and_house()
    # plotter.singleHouse(street,house)

    #

