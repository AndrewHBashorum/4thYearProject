from os_paw.wfs_api import WFS_API
from constants import OS_API_KEY
import pickle
import matplotlib.pyplot as plt
import numpy as np
# Generate an API key from https://osdatahub.os.uk/products

from os import path
import sys
from pathlib import Path
home = str(Path.home())
sys.path.append("/Applications/QGIS3.10.app/Contents/Resources/python/")
sys.path.append("/Applications/QGIS3.10.app/Contents/Resources/python/qgis/PyQt")
sys.path.append("/Users/lukecoburn/opt/anaconda3/lib/python3.8/site-packages")
# sys.path.append("/Applications/QGIS3.10.app/Contents/Frameworks/")
# sys.path.append("/Applications/QGIS3.10.app/Contents/Resources/python")
import os

# os.environ['DYLD_FRAMEWORK_PATH'] = '/Users/lukecoburn/opt/anaconda3/lib/python3.8/site-packages'
# os.environ['QGIS_PREFIX'] = '/Applications/QGIS3.10.app/Contents/Resources/'
# os.environ['PYTHONPATH'] = '/Applications/QGIS3.10.app/Contents/Resources'
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/Applications/QGIS3.10.app/Contents/Plugins/platforms/PyQt5'
# os.environ['LD_LIBRARY_PATH'] = '/Applications/QGIS3.10.app/Contents/MacOS/lib'

# os.environ['DYLD_FRAMEWORK_PATH']="/QGIS.app/Contents/Frameworks"
# os.environ['QGIS_PREFIX']="/QGIS.app/Contents/Resources"
# os.environ['PYTHONPATH']="/Applications/QGIS3.10.app/Contents/Resources/python"
# os.environ['PYTHONPATH']="/Users/lukecoburn/stuff/anaconda/lib/python2.7/site-packages"
# os.environ['PYTHONPATH']="/Users/lukecoburn/stuff/anaconda/python2-pyproj-1.9.5.1-6-x86_64/usr/lib/python2.7/site-packages/pyproj"
# os.environ['DYLD_FRAMEWORK_PATH']="/Applications/QGIS3.10.app/Contents/Frameworks"
# os.environ['QGIS_PREFIX']="/Applications/QGIS3.10.app/Contents/Resources"
# os.environ['PYTHONPATH']="Users/lukecoburn/anaconda3/lib/python3.6/sqlite3/"

# from qgis.core import *
# import QtCore
# from core import *
# import sys
# sys.path.append("C:\Program Files\QGIS Pisa\apps\Python27\Lib")

# import qgis.core
# import qgis.gui
# from gui import *
# from QtGui import *
# from QtCore import *

from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    import pickle5 as pickle
else:
    user = 'luke'
    import pickle

# Choose a Spatial Reference System
SRS = 'EPSG:27700'

# Choose an OS Web Feature Service product
# TYPE_NAME = 'Zoomstack_RoadsRegional'
TYPE_NAME = 'Zoomstack_LocalBuildings'
# TYPE_NAME = 'Zoomstack_Sites'

# Create Bounding Box
with open('site_finder_lynmouth_odd.pickle', 'rb') as f:
    loadedDict = pickle.load(f)
site_dict = loadedDict['site_dict']
id = 1
x_poly = site_dict[id].x_poly
y_poly = site_dict[id].y_poly
plt.fill(x_poly, y_poly, color='b', fill=False)
x0, x1, y0, y1 = min(x_poly), max(x_poly), min(y_poly), max(y_poly)
plt.fill([x0, x1, x1, x0], [y0, y0, y1, y1], color='r', fill=False)
BBOX = '440000, 112000, 443000, 115000'
BBOX = str(round(x0)) + ', ' + str(round(y0)) + ', ' + str(round(x1)) + ', ' + str(round(y1))

# Create WFS_API object and run query
wfs_api = WFS_API(api_key=OS_API_KEY)
payload = wfs_api.get_all_features_within_bbox(type_name=TYPE_NAME, bbox=BBOX, srs=SRS)
features = payload.features
for f in features:
    g = f['geometry']['coordinates'][0]
    x_temp, y_temp = [], []
    print('_______')
    for p in g:
        print(p)
        x_temp.append(p[0])
        y_temp.append(p[1])
    # plt.fill(x_temp, y_temp, color=np.random.rand(3,), fill=False)
