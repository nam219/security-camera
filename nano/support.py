import os, sys

def calculate_number_of_frames(str):
    split = str.split('/')
    return len(split[len(split)-1])

def run_pyface(arg1, arg2):
    os.system('python3 ../networks/face.py {0} {1}'.format(arg1, arg2))
    return True if os.path.isfile("{}/motion-detected".format(arg2)) else False

def run_facenet(argv):
    return False

def run_objectnet(argv):
    return False