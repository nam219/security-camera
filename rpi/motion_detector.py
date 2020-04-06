import io
import picamera
from PIL import Image
import imagehash
import os, subprocess
from support_functions import *


prior_image = None
def detect_motion(camera, cutoff, base_image):
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
        #hash0 = imagehash.average_hash(prior_image)
        current_hash = imagehash.average_hash(current_image)
        base_hash = imagehash.average_hash(base_image)
        #cutoff = 5

        """ if hash1 - base_hash < cutoff:
            print("ending")
            return False """

        if base_hash - current_hash > cutoff:
          print('movement, ' + str(base_hash) + ', ' + str(current_hash) + ', ' + str(base_hash-current_hash))
          return True


        #result = random.randint(0, 10) == 0
        # Once motion detection is done, make the prior image the current
        prior_image = current_image
        #print("false")
        return False

with picamera.PiCamera() as camera:
    print('Starting camera...')
    camera.resolution = (640, 480)
    camera.framerate = 25
    camera.rotation = 180
    stream = picamera.PiCameraCircularIO(camera, seconds=5)
    camera.start_recording(stream, format='h264')
    network = sys.argv[1]
    #give camera some time to warm up
    #can be simplified but this makes it seem somethings happening.
    print('Warming up camera.')
    time.sleep(1)
    print('Camera started.')
    time.sleep(1)
    try:
        
        base_image = create_base_image(camera)
        print('Beginning motion detection.')
        while True:
            camera.wait_recording(1)    
            if detect_motion(camera, 5, base_image):
                print('Motion detected!')
                #base path of videos
                path = '/media/pi/SG1TB/videos/'
                #create the name of the folder for the current day
                foldername = create_folder_name(datetime.datetime.now())
                #make folder if it does not already exist - path/date folder
                didmake, fpath = make_folder(path, foldername)
                if not didmake:
                    print('Error creating folder!')
                    continue
                filenum = create_file_location(fpath)
                #create location string to save videos
                writepath = crate_final_loc_string(fpath, filenum)
                # As soon as we detect motion, split the recording to
                # record the frames "after" motion
                camera.split_recording(writepath + 'after.h264')
                # Write the 5 seconds "before" motion to disk as well
                stream.copy_to(writepath + 'before.h264')
                stream.clear()

                # Wait until motion is no longer detected, then split
                # recording back to the in-memory circular buffer
                #uses a lower threshold for motion so that it doesn't cut off early.
                motion_count=0
                while detect_motion(camera, 4, base_image):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
                vidpath = combine_recordings(writepath, filenum)
                split_to_pics(vidpath, filenum)
                #dont really care about the child returning. Offloads to another device and continues loop
                jet_path = "../recordings/{0}/{1}/".format(foldername, filenum)
                #os.system("python3 ./start_jetson.py {0} {1}".format(jet_path, sys.argv[1]))
                subprocess.run("python3 start_jetson.py {0} {1}".format(jet_path, sys.argv[1]))
    #not really necessary but I hate the errors on exit. might change to catch specific exit keys.
    except KeyboardInterrupt:
        camera.stop_recording()
    finally:
        camera.stop_recording()
