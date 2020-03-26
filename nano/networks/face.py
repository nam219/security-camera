from facenet_pytorch import MTCNN
import torch
import numpy as np
#import mmcv, cv2
from PIL import Image, ImageDraw
#from IPython import display

import jetson.inference
import jetson.utils
import argparse
import sys, os

from nano.support import *

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in an image using an object detection DNN.", 
						   formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage())

parser.add_argument("file_in", type=str, help="filename of the input image to process")
parser.add_argument("file_out", type=str, default=None, nargs='?', help="filename of the output image to save")
#parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
#parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
#parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")

try:
	opt = parser.parse_known_args()[0]
	print (opt)
except:
	print("You need to enter the path to the files and a save location.")
	parser.print_help()
	sys.exit(0)



device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))


mtcnn = MTCNN(keep_all=True, device=device)

path = opt.file_in
output_path = opt.file_out
#frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]

#display.Video('video.mp4', width=640)

face_dected = False
frame_name = calculate_number_of_frames()
frames_tracked = []
for i, frames in enumerate(sys.argv[2:len(frames)]-1):
    frame = Image.open(frames)
    print('\rTracking frame: {}'.format(frames[-(frame_name+1):]))

    # Detect faces
    boxes, _ = mtcnn.detect(frame)
    
    # Draw faces
    frame_draw = frame.copy()
    draw = ImageDraw.Draw(frame_draw)
    try:
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
        face_dected = True
    except Exception:
        print ("No face detected. Continuing to next image.")
        pass
    # Add to frame list
    frames_tracked.append(frame_draw)
print('\nDone')

'''d = display.display(frames_tracked[0], display_id=True)
i = 1
try:
    while True:
        d.update(frames_tracked[i % len(frames_tracked)])
        i += 1
except KeyboardInterrupt:
    pass'''

#dim = frames_tracked[0].size
#fourcc = cv2.VideoWriter_fourcc(*'FMP4')    
#video_tracked = cv2.VideoWriter('video_tracked.mp4', fourcc, 25.0, dim)
save_string = '{0}frame%0{1}d.png'.format(output_path, frame_name)
for i, frame in enumerate(frames_tracked):
#    maker = '{0}frame{1}.jpg'.format(output_path, i)
    frame.save(save_string)
    #video_tracked.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
#video_tracked.release()

os.system("touch {0}motion-detected")