import json
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Image
from PIL import Image
import psutil
import pygame
import time

def clearConsole():
    print(20*('\n'))
    pass

def imshow(filename):
    # pygame.init()
    img = pygame.image.load(filename)
    size = img.get_rect().size
    screen = pygame.display.set_mode(size)
    screen.blit(img, (0, 0))
    pygame.display.flip()
    # pygame.event.clear()

def imclose():
    # pygame.quit()
    pygame.display.quit()


def jsonMaker(json_path, dict):

    if os.path.exists(json_path):
        with open(json_path, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            json_object['chimney'] = dict['chimney']
            json_object = json.dumps(json_object, indent=4)

    else:
        json_object = json.dumps(dict, indent=4)

        # Writing to sample.json
    with open(json_path, "w") as outfile:
        outfile.write(json_object)

def choices(filename,dir):

    image_path = dir + filename
    json_path = dir + 'json/' + filename.replace('png','json')
    # imshow(image_path)

    image = Image.open(image_path)
    image.show()

    outputChoice = input(
        'Does this house have a chimney: 1= Yes , 2= No')

    if outputChoice == '1':
        chimney = 'Yes'
    elif outputChoice == '2':
        chimney = 'No'

    dict = {
        "path" : image_path,
        "chimney": chimney
            }
    # imclose()

    jsonMaker(json_path, dict)

    return outputChoice


if __name__ == '__main__':

    outputChoice = 0
    home = str(Path.home())
    startPath = home + '/Dropbox/auto_processing/height_data_images/'
    streetChoice = input(
        'Enter which street you want to check: 1= Lynmouth , 2= Beverly, 3= Bempton, 4 = Quit')
    listOfPaths = []
    if streetChoice == '1':
        listOfPaths = [startPath + 'LynmouthDriveEven/', startPath +'LynmouthDriveOdd/']
    elif streetChoice == '2':
        listOfPaths = [startPath + 'BeverleyRoadEven/', startPath +'BeverleyRoadOddA/', startPath +'BeverleyRoadOddB/']
    elif streetChoice == '3':
        listOfPaths = [startPath + 'BemptonDriveEven/', startPath +'BemptonDriveOdd/']

    for dir in listOfPaths:
        for filename in os.listdir(dir):
            if filename.endswith(".png"):
                # do smth
                choices(filename,dir)
            else:
                continue

