import io
#import random, math, operator
import picamera
from PIL import Image
import imagehash
from functools import reduce
import os
from rpi.support_functions import *


prior_image = None
def detect_motion(camera, cutoff):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        # Compare current_image to prior_image to detect motion.
        '''h1 = prior_image.histogram()
        h2 = current_image.histogram()
        rms = math.sqrt(reduce(operator.add, map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
        if rms > 50:
            print(rms)
            return True'''
        hash0 = imagehash.average_hash(prior_image)
        hash1 = imagehash.average_hash(current_image)
        #cutoff = 5

        if hash0 - hash1 > cutoff:
          print('movement')
          return True


        #result = random.randint(0, 10) == 0
        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        #print("false")
        return False

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            if detect_motion(camera, 5):
                print('Motion detected!')
                path = '/media/pi/SG1TB/recordings/'
                filename = create_file_name()
                make_folder(path, filename)

                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording(filename + '-' + 'after.h264')
                # Write the 10 seconds "before" motion to disk as well
                stream.copy_to(filename + '-' + 'before.h264')
                stream.clear()

                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                #uses a lower threshold for motion so that it doesn't cut off early.
                while detect_motion(camera, 4):
                    camera.wait_recording(2)

                print('Motion stopped!')
                camera.split_recording(stream)
    #not really necessary but I hate the errors on exit. might change to catch specific exit keys.
    except KeyboardInterrupt:
        camera.stop_recording()
    finally:
        camera.stop_recording()
