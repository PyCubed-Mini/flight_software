# Camera Submodule Code
Files that **need** to go onto camera board for flight:
- `camera_code.py`

## classification_openmv_cam_m7_firmware.bin
This is thet firmware that must be flashed onto the camera board in order for the camera to have access to the trained classification model. You can do this easily with the [OpenMV IDE](https://openmv.io/pages/download) by following [this tutorial](https://docs.edgeimpulse.com/docs/run-inference/running-your-impulse-openmv#deploying-your-impulse-as-an-openmv-firmware). 

## camera_code.py
This is the code that should loaded onto the camera board as `main.py` in order for flight-software to communicate properly with the camera board and send images back and forth with acknowledgements. 

## testing.py
This is a file that can be loaded as `main.py` **for testing only**. This file can be used verify that the classification model and labels are being loaded properly and the camera board is able to run the model to guess what the camera is seeing.