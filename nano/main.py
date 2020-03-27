#import jetson.inference
#import jetson.utils
import sys, argparse, os
from support import *
#take in args from pi.
#run network of choice using those arguments
#if motion detected, send to me. else, delete all files (but not folders jic it gets in way)
if __name__ == '__main__':
	print("opened file with {0} and {1} as arguments".format(sys.argv[1], sys.argv[len(sys.argv)-1]))
	path = "{1}frame/*.png"
	#network selection isnt actually set up yet so this wont work and hopefully just goes to the else
	network = sys.argv[len(sys.argv)-1]
	#use face.py
	if network == "pyface":
		if run_pyface(sys.argv):
			#run the send video script to clean up/combine files and send message
			exit
		else:
			#nothing detected. run a clean up file that compresses video, and deletes the rest without sending anything.
			exit
		print('pyface')
	#use detectnet
	elif network == "facenet":
		if run_facenet(sys.argv):
			#run the send video script to clean up/combine files and send message
			exit
		else:
			#nothing detected. run a clean up file that compresses video, and deletes the rest without sending anything.
			exit
		print('facenet')
	#to do object recognition instead of face.	
	elif network == 'object':
		if run_objectnet(sys.argv):
			#run the send video script to clean up/combine files and send message
			exit
		else:
			#nothing detected. run a clean up file that compresses video, and deletes the rest without sending anything.
			exit
		print('object')
	#defaults to face.py because it is faster
	else:
		if run_pyface(sys.argv):
			#run the send video script to clean up/combine files and send message
			exit
		else:
			#nothing detected. run a clean up file that compresses video, and deletes the rest without sending anything.
			exit
		print('pyface -> default')
