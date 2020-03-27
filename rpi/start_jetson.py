import sys, os

#point was to call this program and then continue on in motion detector, even though this does so little
if __name__ == '__main__':
    os.system('sshfs nick@192.168.1.135:/home/nick/camera_server/security-camera/nano ./jetson-mount')
    os.system("python3 ./jetson-mount/main.py {0} {1}".format(sys.argv[1], sys.argv[len(sys.argv)-1]))