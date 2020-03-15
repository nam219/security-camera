# Introduction

Software for security monitoring with single or multiple cameras with:
- Raspberry Pi
- Jetson Nano

## Functions
- Raspberry Pi: Records video and sends it to a local network stream.
- Jetson Nano: Reads data from stream then processes it for motion and object/face recognition.  Can also be used as a camera.

## Notes
- In order to use python scripts, must use the 'cv' workspace (workon cv) as all python requirements are installed there.
- Run basic camera stream using 'bash launch.sh'. Does not need cv workspace. 
  - Must change device in file to represent what it is used as.
