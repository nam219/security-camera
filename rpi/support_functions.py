import io
#import random, math, operator
import picamera
from PIL import Image
import imagehash
from functools import reduce
import os


def make_folder(path, foldername):
    count = 0
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        while True:
            if not os.path.exists(path):
                os.makedirs(path)
                return True
            else:
                count += 1
                newpath = path + '-' + str(count)
                path = newpath
    return False #i think this isnt reachable but jic


def create_file_name():
    time = datetime.datetime.now()
    filename = 'motion' + datetime.datetime.strftime('%Y%m%d-%H%M%s')