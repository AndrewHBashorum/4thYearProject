import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Image
from PIL import Image
import psutil

def clearConsole():
    print(20*('\n'))
    pass


if __name__ == '__main__':

    outputChoice = 0
    home = str(Path.home())
    startPath = home + '/Dropbox/auto_processing/height_data_images/'
    streetChoice = input(
        'Enter which street you want to check: 1= Lynmouth , 2= Beverly, 3= Bempton, 4 = Quit')

    listOfPaths = [startPath + 'LynmouthDriveEven/', startPath +'LynmouthDriveOdd/']



    def choices(filename,dir):

        image_path = dir + filename
        # print(image_path)
        # display(Image(filename=image_path))
        image = Image.open(image_path)
        image.show()
        outputChoice = input(
            'Enter which street you want to check: 1= Lynmouth , 2= Beverly, 3= Bempton, 4 = Quit')

        for proc in psutil.process_iter():
            if proc.name() == "display":
                proc.kill()

        return outputChoice


    # while outputChoice != '4':
    #     outputChoice = choices()
    #     clearConsole()

    for dir in listOfPaths:
        for filename in os.listdir(dir):
            if filename.endswith(".png"):
                # do smth
                choices(filename,dir)
            else:
                continue

