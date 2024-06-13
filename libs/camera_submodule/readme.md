# Camera Submodule Code
Files that **need** to go onto camera board for flight:
- `camera_code.py`

## Setting up the camera
I recommend that you install the [OpenMV IDE](https://openmv.io/pages/download) as this streamlines the process of using the camera. The quick tutorial I have created follows the process of using this IDE.

First open the OpenMV IDE. Then plug your camera into your computer via USB. The connect button just above the run button in the bottom left corner should change its icon. This lets you know the camera is able to be recognized. Click the connect button. This will likely prompt you to upgrade the firmware and register the device. Do it if you want, but it is not necessary. We will be loading new firmware anyway. 

Once you are past the prompts the camera should be connected and also show up as a drive on your file system. In order to test that the camera is set up properly with our flight software you will need to first [flash the firmware](https://docs.edgeimpulse.com/docs/run-inference/running-your-impulse-openmv#deploying-your-impulse-as-an-openmv-firmware), then load the camera_code.py file as main.py on the camera board drive.

To run our system check test you also need to load a test image onto the camera board at `images/test_image.jpeg` and put the same exact image on the main board at `/sd/images/test_image.jpeg`.

## classification_openmv_cam_m7_firmware.bin
This is the firmware that must be flashed onto the camera board in order for the camera to have access to the trained classification model. You can do this easily with the [OpenMV IDE](https://openmv.io/pages/download) by following [this tutorial](https://docs.edgeimpulse.com/docs/run-inference/running-your-impulse-openmv#deploying-your-impulse-as-an-openmv-firmware). 

## camera_code.py
This is the code that should loaded onto the camera board as `main.py` in order for flight-software to communicate properly with the camera board and send images back and forth with acknowledgements. 

## testing.py
This is a file that can be loaded as `main.py` **for testing only**. This file can be used verify that the classification model and labels are being loaded properly and the camera board is able to run the model to guess what the camera is seeing.