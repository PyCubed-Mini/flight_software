"""
Python system check script for PyCubed satellite board
PyCubed Mini mainboard-v02 for Pocketqube Mission
IMU Sensor Test
* Author(s): Yashika Batra
"""

import time
from ulab import numpy
from lib import pycubed as cubesat


wait_time = 3
norm = numpy.linalg.norm


def request_imu_data(prompt):
    """
    Ask the user to type y/any key to start/cancel the test
    If y, gather IMU data
    Accelerometer and Gyroscope readings are collected 10 times
    in wait_time seconds
    Magnetometer readings are collected at the start and end
    of wait_time seconds
    If any other key, return None for all readings
    """
    # ask user whether or not to start the test
    print(prompt, end="")
    start_test = input("Type Y to start the test, any key to cancel: ")

    # if user opts to cancel the test, return None, handle in the next function
    if start_test.lower() != "y":
        return None, None, None

    # else proceed with the test
    time.sleep(0.5)
    print("Collecting IMU data...")

    # collect magnetometer reading at the start of wait time
    start_mag = numpy.array(cubesat.magnetic())

    # collect total accelerometer and gyroscope readings
    # do 10 reads over wait_time
    acc_total = numpy.array([0., 0., 0.])
    gyro_total = numpy.array([0., 0., 0.])
    for i in range(10):
        acc_total += numpy.array(cubesat.acceleration())
        gyro_total += numpy.array(cubesat.gyro())
        time.sleep(wait_time / 10)

    # collect magnetometer reading at the end of wait time
    end_mag = numpy.array(cubesat.magnetic())

    # calculate the average acc and gyro readings
    acc_final = acc_total / 10
    gyro_final = gyro_total / 10

    # calculate the change in the total magnetometer reading
    mag = norm(end_mag - start_mag)

    # return acc, gyro, change in mag
    print("Data Collection Complete")
    return acc_final, gyro_final, mag


def check_gravity_acc(acc, direction):
    if direction.lower() == "x":
        return (abs(abs(acc[0]) - 9.8) < 1 and abs(acc[1]) < 1
                and abs(acc[2]) < 1)
    elif direction.lower() == "y":
        return (abs(acc[0]) < 1 and abs(abs(acc[1]) - 9.8) < 1
                and abs(acc[2]) < 1)
    elif direction.lower() == "z":
        return (abs(acc[0]) < 1 and abs(acc[1]) < 1
                and abs(abs(acc[2]) - 9.8) < 1)


def gravity_imu_test(result_dict):
    # test the first direction
    prompt = "Please leave the cubesat flat on one side.\n"
    acc, gyro, mag = request_imu_data(prompt)
    grav_xdir = check_gravity_acc(acc, "x")
    grav_ydir = check_gravity_acc(acc, "y")
    grav_zdir = check_gravity_acc(acc, "z")
    # if none of these are true, test has failed
    if not (grav_xdir or grav_ydir or grav_zdir):
        # fail test
        result_string = "Failed reading g m/s^2 in all directions"
        print(result_string)
        result_dict["IMU_AccGravity"] = (result_string, False)
        return result_dict

    # test the next direction
    prompt = "Please leave the cubesat flat on another side.\n"
    acc, gyro, mag = request_imu_data(prompt)
    # if first dir was x, test y and z
    if grav_xdir:
        grav_ydir = check_gravity_acc(acc, "y")
        grav_zdir = check_gravity_acc(acc, "z")
        if not (grav_ydir or grav_zdir):
            # fail test
            result_string = """X direction successful in reading g m/s^2,
failed Y and Z."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict
    # if first dir was y, test x and z
    elif grav_ydir:
        grav_xdir = check_gravity_acc(acc, "x")
        grav_zdir = check_gravity_acc(acc, "z")
        if not (grav_xdir or grav_zdir):
            # fail test
            result_string = """Y direction successful in reading g m/s^2,
failed X and Z."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict
    # if first dir was z, test x and y
    elif grav_zdir:
        grav_xdir = check_gravity_acc(acc, "x")
        grav_ydir = check_gravity_acc(acc, "y")
        if not (grav_xdir or grav_ydir):
            # fail test
            result_string = """Z direction successful in reading g m/s^2,
failed X and Y."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict

    # test the next direction
    prompt = "Please leave the cubesat flat on another side.\n"
    acc, gyro, mag = request_imu_data(prompt)
    # if x and y, test z
    if grav_xdir and grav_ydir:
        grav_zdir = check_gravity_acc(acc, "z")
        if not grav_zdir:
            # fail test
            result_string = """X and Y direction successful in reading g m/s^2,
failed Z."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict
    # if y and z, test x
    elif grav_ydir and grav_zdir:
        grav_xdir = check_gravity_acc(acc, "x")
        if not grav_xdir:
            # fail test
            result_string = """Y and Z direction successful in reading g m/s^2,
failed X."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict
    # if x and z, test y
    elif grav_xdir and grav_zdir:
        grav_ydir = check_gravity_acc(acc, "y")
        if not grav_ydir:
            # fail test
            result_string = """X and Z direction successful in reading g m/s^2,
failed Y."""
            print(result_string)
            result_dict["IMU_AccGravity"] = (result_string, False)
            return result_dict

    # if everything has passed and we haven't exited yet, update
    result_string = """X, Y, and Z directions successful in reading g m/s^2."""
    print(result_string)
    result_dict["IMU_AccGravity"] = (result_string, True)
    return result_dict


def stationary_imu_test(result_dict):
    """
    Return acceleration, gyro, and magnetic readings from request_imu_data
    If None, update result dictionary that test was not run
    Else, check that the norms of the average accelerometer and gyroscope
    readings are near 0 and update result dictionary
    """
    # prompt user and get imu data
    prompt = "Please leave the cubesat stationary on a table.\n"
    acc, gyro, mag = request_imu_data(prompt)

    if acc is None and gyro is None:
        result_dict["IMU_GyroStationary"] = (
            "Stationary test not completed.", None)
        return result_dict

    # else continue running the test
    gyro_string = f"Gyro: {tuple(gyro)} (deg/s)"

    # if total gyro ~= 0 deg/s, true
    gyro_is_stationary = norm(gyro) < 1

    # print result to user
    if gyro_is_stationary:
        print("Stationary gyroscope reading is near 0 deg/s.")
    else:
        print("Stationary gyroscope reading is not near 0 deg/s.")

    # update result dictionary
    result_dict["IMU_GyroStationary"] = (gyro_string, gyro_is_stationary)
    return result_dict


def rotating_imu_test(result_dict):
    """
    Return acceleration, gyro, and magnetic readings from request_imu_data
    If None, update result dictionary that test was not run
    Else, check that the norm of the average gyroscope reading is positive
    and update result dictionary
    """
    # record gyro reading
    prompt = f"""Please rotate the cubesat as best as possible for {wait_time}
seconds once you start the test.\n"""
    acc, gyro, mag = request_imu_data(prompt)
    if gyro is None:
        # user entered "n", cancel the test
        result_dict["IMU_GyroRotating"] = (
            "Rotating test not completed.", None)
        return result_dict

    # else continue running the test
    gyro_string = (f"Gyro: {tuple(gyro)} (deg/s)")
    gyro_is_rotating = norm(gyro) >= 1

    # print result to user
    if gyro_is_rotating:
        print("Rotating gyroscope reading is approx. greater than 0 deg/s.")
    else:
        print("Rotating gyroscope reading is near 0 deg/s.")

    # update result dictionary
    result_dict["IMU_GyroRotating"] = (gyro_string, gyro_is_rotating)
    return result_dict


def magnet_imu_test(result_dict):
    """
    Return acceleration, gyro, and magnetic readings from request_imu_data
    If None, update result dictionary that test was not run
    Else, check that the magnetometer reading increased as the magnet
    moved closer, and update result dictionary
    """
    # record magnetometer reading
    prompt = f"""Please slowly move the magnet closer to the cubesat for
{wait_time} seconds once you start the test.\n"""
    acc, gyro, mag = request_imu_data(prompt)
    if mag is None:
        # user entered "n", cancel the test
        result_dict["IMU_MagMagnet"] = ("Magnet test not completed.", None)
        return result_dict

    # else continue running the test
    mag_string = (f"Change in Mag Reading: {mag} (µT)")
    mag_is_increasing = mag >= 10

    # print result to user
    if mag_is_increasing:
        print("Magnetometer reading is increasing.")
    else:
        print("Magnetometer reading is not increasing.")

    # update result dictionary
    result_dict["IMU_MagMagnet"] = (mag_string, mag_is_increasing)
    return result_dict


def temp_imu_test(result_dict):
    """
    Get temperature reading from IMU and ask the user to verify that
    this reading is correct. Give users a general range for room temperature
    to help verify, and update result dictionary as per user response
    """
    # collect temperature reading, ask user to confirm
    temp = cubesat.temperature_imu()
    print(f"IMU Temperature Reading: {temp} degrees Celsius")

    # check that temperature is between 20 and 80 degrees Celsius
    result_val_bool = temp >= 20 and temp <= 80

    # update result dict based on user input
    result_dict["IMU_Temp"] = (f"Temperature: {temp}", result_val_bool)
    return result_dict


def run(hardware_dict, result_dict):
    """
    Check the IMU when the cubesat is stationary, moving, rotating,
    and around a magnetic field. Also check the IMU temperature sensor
    If initialized correctly, run test and update result dictionary
    If not initialized, update result dictionary
    """

    # if no IMU detected, update result dictionary and return
    if not hardware_dict["IMU"]:
        result_dict["IMU_AccGravity"] = (
            "Cannot test accelerometer; no IMU detected", None)
        result_dict["IMU_GyroStationary"] = (
            "Cannot test gyroscope; no IMU detected", None)
        result_dict["IMU_GyroRotating"] = (
            "Cannot test gyroscope; no IMU detected", None)
        result_dict["IMU_MagMagnet"] = (
            "Cannot test magnetometer; no IMU detected", None)
        result_dict["IMU_Temp"] = (
            "Cannot test temperature sensor; no IMU detected", None)
        return result_dict

    # if IMU detected, run other tests
    else:
        print("Starting IMU Stationary Test...")
        stationary_imu_test(result_dict)
        print("IMU Stationary Test complete.\n")

        print("Starting IMU Gravity Test...")
        gravity_imu_test(result_dict)
        print("IMU Gravity Test complete.\n")

        print("Starting IMU Rotating Test...")
        rotating_imu_test(result_dict)
        print("IMU Rotating Test complete.\n")

        print("Starting IMU Magnet Test...")
        magnet_imu_test(result_dict)
        print("IMU Magnet Test complete.\n")

        print("Starting IMU Temperature Test...")
        temp_imu_test(result_dict)
        print("IMU Temperature Test complete.\n")

    return result_dict
