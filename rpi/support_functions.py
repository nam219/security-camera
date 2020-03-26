import io, subprocess, os, sys
import datetime, time
from PIL import Image
import picamera
#import ffmpy


def create_file_location(folder):
    count = 0
    while True:
        loc = folder + '/' + str(count)
        if (os.path.exists(loc)):
            count += 1
        else:
            os.makedirs(loc)
            return str(count)
    #filename = datetime.datetime.strftime(ftime, '%y%m%d-%H%M%S')
    #filename = 'motion' + timestring
    #return filename

def create_folder_name(time):
    date = datetime.datetime.strftime(time, '%Y-%m-%d')
    return date
 
def make_folder(path, foldername):
    #count = 0
    combine = path + '/' + foldername
    if(os.path.exists(combine)):
        return True, combine
    elif not os.path.exists(combine):
        os.makedirs(combine)
        return True, combine
    return False #i think this isnt reachable but jic

def create_base_image(camera):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    return Image.open(stream)

def crate_final_loc_string(path, fnum):
    ret = path + '/' + fnum + '/'
    return ret

def convert_to_mp4(name, num):
    output = "{0}/{1}".format(name[:-(len(str(num))+5)], num)
    print("ffmpeg -i {0} -c {1}.mp4".format(name, output))
    os.system("ffmpeg -i {0} -c copy {1}.mp4".format(name, output))
    
    
def combine_recordings(path, num):
    before = path + '/' + 'before.h264'
    after = path + '/' + 'after.h264'
    concat_string = 'concat:{0}|{1}'.format(before, after)
    combined = path + str(num) + '.h264'
    os.system("ffmpeg -i \"{0}\" -c copy {1}".format(concat_string, combined))
    os.system('rm {0} {1}'.format(before, after))
    print("ffmpeg -i \"{0}\" -c copy {1}".format(concat_string, combined))
    convert_to_mp4(combined, num)
    #return is only used to create the string to pass into split_to_pics. Will eventually fix. 
    return combined[:-(len(str(num))+5)]

#path creation is so convoluted. Will eventually fix if gets annoying.
def split_to_pics(vidpath, number):
    made, path = make_folder(vidpath, "frames")
    #time.sleep(1)
    if not made:
        print("Error creating pic folder!")
        exit()
    command = "ffmpeg -i {0}{1}.h264 {0}/frames/frame%05d.png".format(vidpath, str(number)) #-qscale:v 2
    print(command)
    os.system(command)
    


