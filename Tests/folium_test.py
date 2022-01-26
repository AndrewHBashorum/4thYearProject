import pandas as pd
import folium
import display
from openpyxl import load_workbook
import math


def auto_open(path, map):
    html_page = f'{path}'
    f_map.save(html_page)
    # open in browser.
    new = 2
    webbrowser.open(html_page, new=new)

map_ = folium.Map(location=[51.565699, -0.403421], zoom_start=10)

# wb = load_workbook(filename='folium_test.xlsx')
# ws = wb["Sheet1"]
# data = ws.values
# columns = next(data)[0:]
# # Create a DataFrame based on the second and subsequent lines of data
# df = pd.DataFrame(data, columns=columns)
#
#
# locs = df[['lat', 'long']]
# loc_list = locs.values.tolist()

# To display all data use the following two lines, but, since your data has
# so many points, this process will be time-consuming.
# for point in range(0, len(loc_list)):
#     if not math.isnan(loc_list[point][0]):
#         folium.Marker(loc_list[point]).add_to(map_)

# To display first 1000 points
# for point in range(0, 1000):
#     folium.Marker(loc_list[point]).add_to(map_)
# save method of Map object will create a map
# map_.save("my_map1.html")
display(map_)