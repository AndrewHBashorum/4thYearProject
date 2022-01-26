import os
import matplotlib.pyplot as plt
import pickle
from utils.geometry import Geometry
gt = Geometry()

fig = plt.figure()
tolerance = 20
with open('../PickleFiles/site_finder_lynmouth_odd.pickle', 'rb') as f:
    loadedDict = pickle.load(f)
site_dict = loadedDict['site_dict']
neigh_site_dict = loadedDict['neigh_site_dict']
house_dict = loadedDict['house_dict']

site_id = 5
x_poly = site_dict[site_id].x_poly
y_poly = site_dict[site_id].y_poly
xt = site_dict[site_id].xt
yt = site_dict[site_id].yt

command = '/Applications/QGIS-LTR.app/Contents/MacOS/bin/./run.sh'
command += str(' ') + str(xt)
command += str(' ') + str(yt)
command += str(' ') + str(tolerance)
os.system(command)

cur_dir = os.path.dirname(os.path.realpath(__file__))
file = open(cur_dir + "/temp.pickle", 'rb')
dict = pickle.load(file)
xp, yp, tolerance, X, Y = dict['xp'], dict['yp'], dict['tolerance'], dict['X'], dict['Y']

# Make plot
plt.plot(xp, yp, 'x')
plt.fill(x_poly, y_poly, color='b', linewidth=2, fill=False)
plt.fill([xp - tolerance, xp + tolerance, xp + tolerance, xp - tolerance], [yp - tolerance,yp - tolerance, yp + tolerance, yp + tolerance], color='orange',fill=False)
cx = sum(x_poly)/len(x_poly)
cy = sum(y_poly)/len(y_poly)
poly_in_poly = True
for i in range(len(X)):
    if gt.polygon_in_enlarged_polygon(X[i], Y[i], x_poly, y_poly, 1.1):
        plt.fill(X[i], Y[i], color='lightgreen')
    plt.fill(X[i], Y[i], color='r', linewidth=2, fill=False)

