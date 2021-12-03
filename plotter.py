

import matplotlib.pyplot as plt
import pickle

class Plotter(object):

    def __init__(self):
        self.open_pickle()
        pass

    def plotSites(self):
        plt.figure()

        for i in self.neigh_site_id_list:
            if self.neigh_site_dict[i].active:
                plt.fill(self.neigh_site_dict[i].x_poly, self.neigh_site_dict[i].y_poly, ':', fill=False, color='r', linewidth=3)

        for i in self.site_id_list:
            plt.fill(self.site_dict[i].x_poly, self.site_dict[i].y_poly, fill=False, color='b')



    def open_pickle(self):

        with open('house_site_pickle/site_finder_all.pickle', 'rb') as f:
            self.loadedDict = pickle.load(f)


    def singleStreetSide(self, streetSide):
        self.site_dict = self.loadedDict[streetSide]['site_dict']
        self.neigh_site_dict = self.loadedDict[streetSide]['neigh_site_dict']
        self.house_dict = self.loadedDict[streetSide]['house_dict']

        self.site_id_list = self.site_dict.keys()
        self.neigh_site_id_list = self.neigh_site_dict.keys()

        self.plotSites()



    def singleHouse(self, streetSide, house):
        self.site_dict = self.loadedDict[streetSide]['site_dict']

        self.site_id_list = self.loadedDict[streetSide]['house_dict'][house].sites
        self.neigh_site_dict = self.loadedDict[streetSide]['neigh_site_dict']

        self.neigh_site_id_list = self.site_dict[self.site_id_list[0]].neigh_sites_id

        self.plotSites()

    def entire(self):

        self.neigh_site_dict_list = []
        self.site_dict_list = []
        self.house_dict_list = []
        self.site_id_list = []
        self.neigh_site_id_list = []

        for i in self.loadedDict.keys():
            print(i)
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

        # for i in self.site_id_list:
        #     plt.fill(self.site_dict_list[i].x_poly, self.site_dict_list[i].y_poly, fill=False, color='b')
        #


if __name__ == '__main__':

    street = 'lynmouthDriveEven'
    house = '52_HA4_9BY'
    #house = '53_HA4_9BY'

    plotter = Plotter()
    # plotter.singleStreetSide(street)
    # plotter.singleHouse(street,house)
    plotter.entire()
