import urllib.request
from PIL import Image, ImageDraw
from utils.constants import GOOGLE_API_KEY
from geometry import Geometry
import pickle
import math
import warnings
import numpy as np
import os

from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    aerial_im_str = '/Users/andrewbashorum/Dropbox/auto_processing/aerial_images'
else:
    user = 'luke'
    aerial_im_str = '/Users/lukecoburn/Dropbox/auto_processing/aerial_images'

warnings.filterwarnings("ignore", category=FutureWarning)

class SatelliteImage(object):
    def __init__(self):
        self.gt = Geometry()
        self.url1 = "https://maps.googleapis.com/maps/api/staticmap?center="
        self.url2 = "&zoom=20&size=200x200&maptype=satellite&format=png&scale=2&key=" + GOOGLE_API_KEY

    def load_from_pickle(self, pickle_file):
        with open(pickle_file + '.pickle', 'rb') as f:
            loadedDict = pickle.load(f)
        self.site_dict = loadedDict['site_dict']
        self.neigh_site_dict = loadedDict['neigh_site_dict']
        self.house_dict = loadedDict['house_dict']
        self.site_keys = list(self.site_dict.keys())
        self.house_keys = list(self.house_dict.keys())
        self.pickle_file = os.path.basename(pickle_file).split('2')[0]

    def save_to_pickle(self, pickle_file):
        dict = {
            'house_dict': self.house_dict,
            'site_dict': self.site_dict,
            'neigh_site_dict': self.neigh_site_dict
        }
        with open(pickle_file + '.pickle', 'wb') as f:
            pickle.dump(dict, f)

    def load_image(self, site_id):
        print(site_id,'/',len(self.site_keys))
        house_id = self.site_dict[site_id].house_address[0]
        dx, dy = 0.000016, 0.000016
        lon, lat = self.gt.convert_27700_to_lat_lon(self.house_dict[house_id].xt, self.house_dict[house_id].yt)
        url = self.url1 + str(round(lat + dy, 6)) + ',%20' + str(round(lon + dx, 6)) + self.url2
        urllib.request.urlretrieve(url, "temp.png")
        img = Image.open("temp.png")
        xcp, ycp = self.pixels_to_coords(lon, lat, img, url)
        # print('image corner coords', xcp, ycp)
        xh, yh = self.gt.convert_list_27700_to_lat_lon(self.house_dict[house_id].X_bounds4, self.house_dict[house_id].Y_bounds4)
        # print('bounds', xh, yh)
        xp, yp = self.coords_to_pixels(xh, yh, xcp, ycp, img)
        # xp, yp = self.gt.shift_polygon(xp, yp, 40, -10)
        # xp, yp = self.gt.rotate_polygon(xp, yp, np.pi)
        xp, yp = self.gt.enlarge_polygon(xp, yp, 1.65)
        xy = [(xp[i], yp[i]) for i in range(len(xp))]

        draw = ImageDraw.Draw(img)
        draw.polygon(xy)
        # img.show()
        # img = img.rotate(180)

        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(xy, fill=255, outline=None)
        black = Image.new("RGBA", img.size, (0, 0, 0, 0))
        result = Image.composite(img, black, mask)
        result.save("result.png")
        orientation = self.house_dict[house_id].orientation
        angle = 360*(np.pi/2 - orientation)/(2*np.pi)
        result = result.rotate(angle)
        result = result.crop(result.getbbox())
        im_str = aerial_im_str + '/' + self.pickle_file + '/aerial_' + str(house_id) + '.png'
        result.save(im_str)
        # result.show()
        self.house_dict[house_id].satellite_image = im_str

    def pixels_to_coords(self, lon, lat, img, url):
        w = img.size[0]/2
        h = img.size[1]/2
        x_temp = [0, w, w, 0]
        y_temp = [0, 0, h, h]
        s1 = url.split('&zoom=')[1]
        s2 = s1.split('&size=')[0]
        zoom = int(s2)
        parallelMultiplier = math.cos(lat * math.pi / 180)
        degreesPerPixelX = 360 / math.pow(2, zoom + 8)
        degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier

        x, y = [], []
        for i in range(len(x_temp)):
            x.append(lon + degreesPerPixelX * (x_temp[i] - w / 2))
            y.append(lat - degreesPerPixelY * (y_temp[i] - h / 2))
        return x, y

    def coords_to_pixels(self, x, y, xcp, ycp, img):
        w = img.size[0]
        h = img.size[1]
        xp, yp = [], []
        for i in range(len(x)):
            x_rat = (max(xcp) - x[i])/(max(xcp) - min(xcp))
            y_rat = (max(ycp) - y[i])/(max(ycp) - min(ycp))
            xp.append(round(w*x_rat))
            yp.append(h-round(h*y_rat))
        return xp, yp


if __name__ == '__main__':
    si = SatelliteImage()
    pickle_file_name = 'site_finder_lynmouth_odd2'
    si.load_from_pickle(pickle_file_name)
    for site_id in si.site_keys:
        si.load_image(site_id)
    pickle_file_name = 'site_finder_lynmouth_odd3'
    si.save_to_pickle(pickle_file_name)

    # https://maps.googleapis.com/maps/api/staticmap?center=51.565702,%20-0.403389&zoom=20&size=200x200&maptype=satellite&format=png&scale=2&key=AIzaSyAcQIYA9e_qvw7MBLBzqLXMe4m8VIN2agYif
    # https://maps.googleapis.com/maps/api/staticmap?center=51.567337,%20-0.404980&zoom=20&size=200x200&maptype=satellite&format=png&scale=2&key=rv682gWPTxfWYoNEuyKBdjrnGhZDwHaF


