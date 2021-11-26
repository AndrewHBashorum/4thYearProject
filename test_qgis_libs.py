# import qgis.core
from qgis.core import *
from qgis.gui import *
import os
from constants import OS_API_KEY
# import qgis.gui

app = QgsApplication([], True)
app.setPrefixPath("/Users/lukecoburn/AndrewBashorum_4thYearProject", True)
app.initQgis()
# canvas = QgsMapCanvas()
# canvas.setWindowTitle("PyQGIS Standalone Application Example")
# canvas.setCanvasColor(Qt.white)
# layer =  QgsVectorLayer('LineString?crs=epsg:4326', 'MyLine' , "memory")
# pr = layer.dataProvider()
# linstr = QgsFeature()
# geom = QgsGeometry.fromWkt("LINESTRING (1 1, 10 15, 40 35)")
# linstr.setGeometry(geom)
# pr.addFeatures([linstr])
# layer.updateExtents()
# QgsMapLayerRegistry.instance().addMapLayer(layer)
# canvas.setExtent(layer.extent())
# canvas.setLayerSet([QgsMapCanvasLayer(layer)])
# canvas.zoomToFullExtent()
# canvas.freeze(True)
# canvas.show()
# canvas.refresh()
# canvas.freeze(False)
# canvas.repaint()
# exitcode = app._exec()
# QgsApplication.exitQgis()
# sys.exit(exitcode)

# from qgis.PyQt.QtCore import *
# from qgis.PyQt.QtGui import *
# from qgis.PyQt.QtWidgets import *
# from gui import *
# from QtGui import *
# from QtCore import *

# osBuildingsLayer = QgsVectorLayer(" pagingEnabled='true' preferCoordinatesForWfsT11='false' restrictToRequestBBOX='1' srsname='EPSG:27700' typename='osfeatures:Topography_TopographicArea' url='https://api.os.uk/features/v1/wfs?key=%s' version='auto'" % OS_API_KEY,
#     'OS Topography Polygons', 'WFS')

# osBuildingsLayer.loadNamedStyle(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'assets', 'osfeatures_topographic_area.qml'))
# print(osBuildingsLayer)
#
# xp, yp, tolerance = 510763, 186407, 10
# searchRect = QgsRectangle(xp - tolerance, yp - tolerance, xp + tolerance, yp + tolerance)
# print(QgsRectangle)
# request = QgsFeatureRequest()
# request.setFilterRect(searchRect)
# print(request)
#
#
# print('Here')