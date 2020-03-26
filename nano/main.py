#import jetson.inference
#import jetson.utils
import sys, argparse, os

#take in args from pi.
#run network of choice using those arguments
#if motion detected, send to me. else, delete all files (but not folders jic it gets in way)
if __name__ == '__main__':
	print("opened file with {0} and {1} as arguments".format(sys.argv[1], sys.argv[2]))
	path = "{1}frame/*.png"
	network = sys.argv[2]
	#use face.py
	if network == "pyface":
		
		print('pyface')
	#use detectnet
	elif network == "facenet":
		print('facenet')
	#defaults to face.py because it is faster	
	else:
		print('pyface -> default')
