If you do not use the official OS for the Nano, `numpy` and `opencv` need to be installed. 
Install the official tensorflow release for Jetson Nano by following the instructions from [here](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html).


When running inference on the Nano for the first time, You need to run the `compile_ssd_mobilenet.py` script from your project directory.

```Shell
cd project_directory
python3 compile_ssd_mobilenet.py
```
