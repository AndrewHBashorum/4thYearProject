from qgis.core import *
from qgis.gui import *
import os
from constants import OS_API_KEY
os.environ['DYLD_FRAMEWORK_PATH'] = "/Applications/QGIS3.10.app/Contents/Frameworks/"
os.environ['QGIS_PREFIX'] = "/Applications/QGIS-LTR.app/Contents/Resources/"

app = QgsApplication([], True)

app.setPrefixPath("/Applications/QGIS-LTR.app/Contents/Resources/", True)
app.initQgis()
# print('test')