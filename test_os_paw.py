from os_paw.wfs_api import WFS_API
from constants import OS_API_KEY
import pickle
import matplotlib.pyplot as plt
# Generate an API key from https://osdatahub.os.uk/products

# Choose a Spatial Reference System
SRS = 'EPSG:27700'

# Choose an OS Web Feature Service product
TYPE_NAME = 'Zoomstack_RoadsRegional'

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
payload = wfs_api.get_all_features_within_bbox(type_name=TYPE_NAME,
                                               bbox=BBOX,
                                               srs=SRS)