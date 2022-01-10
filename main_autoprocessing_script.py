from pathlib import Path

if 'lukecoburn' not in str(Path.home()):
    user = 'andrew'
    pickle_file_folder = '/Users/andrewbashorum/Dropbox/auto_processing/pickle_files/'
    excel_file_folder = '/Users/andrewbashorum/Dropbox/auto_processing/excel_files/'
    height_file_folder = '/Users/andrewbashorum/Dropbox/auto_processing/height_data_images/'
else:
    user = 'luke'
    pickle_file_folder = '/Users/lukecoburn/Dropbox/auto_processing/pickle_files/'
    excel_file_folder = '/Users/lukecoburn/Dropbox/auto_processing/excel_files/'
    height_file_folder = '/Users/lukecoburn/Dropbox/auto_processing/height_data_images/'

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import time
import openpyxl

from site_finder import SiteFinder
from house_finder import HouseFinder
from fix_data import FixData
from satellite_image import SatelliteImage
from cookie_cutter import CookieCutter

#start timer
start = time.time()

# Switch on and off parts of the script
run_site_finder = False
run_house_finder = False
run_fix_data = False
run_satellite_image = False
run_cookie_cutter = True
run_machine_part = True

# Choose street for processing
wb = openpyxl.load_workbook(excel_file_folder + 'house_lists.xlsx')
pickle_file_list = list(wb.sheetnames)
pickle_file = pickle_file_list[0]

for pickle_file in [pickle_file_list[0]]:
    print(pickle_file)
    # Run Site Finder
    if run_site_finder:
        load_from_pickle = True
        sf = SiteFinder(pickle_file_folder, excel_file_folder)
        if load_from_pickle:
            sf.main_from_pickle(pickle_file)
        else:
            sf.main(3, pickle_file)
        # sf.save_to_pickle(pickle_file)

    # Run House Finder
    if run_house_finder:
        tolerance = 20
        hf = HouseFinder(20)
        # load all sites and houses from pickle
        hf.load_from_pickle(pickle_file, pickle_file_folder)
        for site_id in hf.site_keys:
            print(pickle_file, site_id, '/', len(hf.site_keys))
            hf.run_shell_script_to_find_house_bounds(site_id)
        hf.save_to_pickle(pickle_file + '1', pickle_file_folder)

    # Run Fix Data
    if run_fix_data:
        fd = FixData()
        fd.main(pickle_file+'1', pickle_file_folder)
        for site_id in fd.site_keys:
            print('site:', site_id, 'neighs:', fd.site_dict[site_id].neigh_sites)
        # fd.save_to_pickle(pickle_file_folder + pickle_file + '2.pickle')

    # Run Satellite Image
    if run_satellite_image:
        si = SatelliteImage()
        si.load_from_pickle(pickle_file_folder + pickle_file + '2')
        for site_id in si.site_keys:
            si.load_image(site_id)
        si.save_to_pickle(pickle_file_folder + pickle_file + '3')

    # Run Cookie Cutter
    if run_cookie_cutter:
        cc = CookieCutter()
        cc.load_from_pickle(pickle_file_folder + pickle_file + '4.pickle')
        # count = 0
        # for house_id in cc.house_keys:
        #     count += 1
        #     print(count, '/', len(cc.house_keys), house_id, pickle_file)
        #     cc.get_height_data(True, house_id, height_file_folder + pickle_file + '/', pickle_file_folder + pickle_file + '_height/')
        # cc.save_to_pickle(pickle_file_folder + pickle_file + '4.pickle')

end = time.time()
print('Time Taken:', round(end - start), 'seconds')
