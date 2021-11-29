import numpy as np
import os
import pickle

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

from constants import OS_API_KEY

import sys
xp = float(sys.argv[1])
yp = float(sys.argv[2])
tolerance = float(sys.argv[3])

cur_dir = os.path.dirname(os.path.realpath(__file__))
os.environ['DYLD_FRAMEWORK_PATH'] = "/Applications/QGIS3.10.app/Contents/Frameworks/"
os.environ['QGIS_PREFIX'] = "/Applications/QGIS-LTR.app/Contents/MacOS/"
os.environ['DYLD_INSERT_LIBRARIES'] = "/Applications/QGIS-LTR.app/Contents/MacOS/lib/libsqlite3.dylib"

app = QgsApplication([], True)
app.setPrefixPath(os.environ['QGIS_PREFIX'], True)
app.initQgis()

osBuildingsLayer = QgsVectorLayer(
    " pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:27700' typename='osfeatures:Topography_TopographicArea' url='https://api.os.uk/features/v1/wfs?key=%s' version='auto'" % OS_API_KEY,
    'OS Topography Polygons', 'WFS')

searchRect = QgsRectangle(xp - tolerance, yp - tolerance, xp + tolerance, yp + tolerance)

request = QgsFeatureRequest()
request.setFilterRect(searchRect)
# request.setFlags(QgsFeatureRequest.ExactIntersect)

dict = {}
dict['xp'] = xp
dict['yp'] = yp
dict['tolerance'] = tolerance
X = []
Y = []
for feature in osBuildingsLayer.getFeatures(request):
    if feature.attributes()[5] == "Buildings":
        geometry = feature.geometry()
        if QgsWkbTypes.singleType(geometry.wkbType()) == QgsWkbTypes.LineString:
            geometry = geometry.convexHull()
        elif QgsWkbTypes.singleType(geometry.wkbType()) == QgsWkbTypes.Polygon:
            p = next(geometry.parts())
            c = p.toCurveType()
            geometry = c.exteriorRing().clone()
        points = geometry.points()
        x = []
        y = []
        for i in range(len(points)):
            x.append(round(points[i].x(), 4))
            y.append(round(points[i].y(), 4))
        X.append(x)
        Y.append(y)

dict['X'] = X
dict['Y'] = Y

fileName = cur_dir + '/temp.pickle'
with open(fileName, 'wb') as handle:
    pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# app.exec()
# app.exitQgis()

