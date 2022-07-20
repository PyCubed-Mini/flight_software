"""
Python system check script for PyCubed satellite board
PyCubed Mini mainboard-v02 for Pocketqube Mission
* Author(s): Yashika Batra
"""

from lib import pycubed
import tests
import tests.imu_test
import tests.radio_test
import tests.sun_sensor_test
import tests.coil_test
import tests.burnwire_test

# initialize hardware_dict and result_dict
hardware_dict = pycubed._cubesat.hardware
result_dict = {
    'SDcard_Logging': ('', False),
    'IMU_AccStill': ('', False),
    'IMU_AccMoving': ('', False),
    'IMU_GyroStill': ('', False),
    'IMU_GyroRotating': ('', False),
    'IMU_MagMagnet': ('', False),
    'IMU_Temp': ('', False),
    'Radio_ReceiveBeacon': ('', False),
    'Radio_SendBeacon': ('', False),
    'Sun-Y_Dark': ('', False),
    'Sun-Y_Light': ('', False),
    'Sun-Z_Dark': ('', False),
    'Sun-Z_Light': ('', False),
    'Sun-X_Dark': ('', False),
    'Sun-X_Light': ('', False),
    'Sun+Y_Dark': ('', False),
    'Sun+Y_Light': ('', False),
    'Sun+Z_Dark': ('', False),
    'Sun+Z_Light': ('', False),
    'Sun+X_Dark': ('', False),
    'Sun+X_Light': ('', False),
    'CoilDriverX': ('', False),
    'CoilDriverY': ('', False),
    'CoilDriverZ': ('', False),
    'Burnwire1': ('', False),
    'Burnwire2': ('', False),
}

# print acknowledgement that test has started
print("Running System Check...")
print("Hardware Successfully Initialized. Printing results...")
print("")
for entry in hardware_dict:
    print(str(entry.key), str(entry.val))
print("")

# test logging
tests.logging_test.run(hardware_dict, result_dict)

# test imu
tests.imu_test.run(hardware_dict, result_dict)

# test sun sensor
tests.sun_sensor_test.run(hardware_dict, result_dict)

# ask to test coil driver
tests.coil_test.run(hardware_dict, result_dict)

# ask to test burnwire
burnwire_input = input("Would you like to test the burnwires? (Y/N): ")
if burnwire_input == "Y":
    tests.burnwire_test.run(hardware_dict, result_dict)

# ask to test radio
radio_input = input("Would you like to test the radio? (Y/N): ")
if radio_input == "Y":
    antenna_attached = input("Is an antenna attached to the radio? (Y/N): ")
    tests.radio_test.run(hardware_dict, result_dict, antenna_attached)

# end test and print results
print("")
print("Test has concluded. Printing results...")
print("")
for entry in hardware_dict:
    print(str(entry.key), str(entry.val))
print("")
