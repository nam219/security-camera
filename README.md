# Introduction

Software for security monitoring with single or multiple cameras with:
- Raspberry Pi 4
- Jetson Nano

## Functions
- Raspberry Pi: Records video and sends it to a local network stream.  
- Jetson Nano: Reads data from stream then processes it for motion and object/face recognition.  
  - Can also be used as a camera that works the same as a Raspberry Pi.

## Notes
- Pretty much any device can take the place of the Raspberry Pi as long as it can use PiCamera.

```Shell
sudo apt-get update
sudo apt-get install python-picamera python3-picamera
```

- Run the script in the launch folder corresponding to the device to begin.
```Shell
bash launchPi.sh
```
or
```Shell
bash launchJetson.sh
```
