# Camera Submodule Code
Files that **need** to go onto camera board for flight:
- `camera_code.py`
- `classification.tflite`
- `labels.txt`


## camera_code.py
This is the code that should loaded onto the camera board as `main.py` in order for flight-software to communicate properly with the camera board and send images back and forth with acknowledgements. 

## testing.py
This is a file that can be loaded as `main.py` **for testing only**. This file can be used verify that the classification model and labels are being loaded properly and the camera board is able to run the model to guess what the camera is seeing.