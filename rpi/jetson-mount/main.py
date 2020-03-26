#import jetson.inference
#import jetson.utils
import sys, argparse, os

#take in args from pi.
#run network of choice using those arguments
#if motion detected, send to me. else, delete all files (but not folders in  jic it gets in way)
if __name__ == '__main__':
	print("opened file with {0} and {1} as arguments".format(sys.argv[1], sys.argv[2]))
