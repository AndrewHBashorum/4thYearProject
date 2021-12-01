
from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    import pickle5 as pickle
else:
    user = 'luke'
    import pickle

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import time
from datetime import date

from site_finder import SiteFinder
import xlrd


# Choose street for processing

wb = xlrd.open_workbook(path_to_my_workbook)
ws = wb.sheet_by_index(0)
mylist = ws.col_values(0)
pickle_file_list = ['LynmouthDriveOdd', 'LynmouthDriveEven', ]
pickle_file = pickle_file_list[0]

# Run Site Finder
start = time.time()
load_from_pickle = True
sf = SiteFinder()
if load_from_pickle:
    sf.main_from_pickle()
else:
    sf.main(3)
    date = today = date.today()
sf.save_to_pickle(pickle_file)

# Run House Finder

# Run Fix Data

# Run Satellite Image

# Run Cookie Cutter
