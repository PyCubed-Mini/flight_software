# flake8: noqa
import os
import time

import sensor
import tf
from pyb import UART

# set up camera
sensor.reset()                          # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)     # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)         # Set frame size to HD (640 x 480)
sensor.skip_frames(time=2000)           # Wait for settings take effect.

# UART 3, and baudrate.
uart = UART(3, 115200)

# constants
CONFIRMATION_SEND_CODE = 0xAA
CONFIRMATION_RECEIVE_CODE = 0xAB
IMAGE_START = 0xAC
IMAGE_MID = 0xAD
IMAGE_END = 0xAE
IMAGE_CONF = 0xAF
PACKET_REQ = 0xB0
NO_IMAGE = 0xB1
CONFIRMATION_RECEIVE_TEST_CODE = 0xB2

test_filepath = "images/test_image.jpeg"
filepath = "images/sat_image.jpeg"

buffer = bytearray(1)

def check_connection() -> None:
    # write confirmation code to UART and wait for response
    # confirms to the mainboard that the camera board is on
    confirmed = False
    while not confirmed:
        buffer[0] = CONFIRMATION_SEND_CODE
        uart.write(buffer)
        start_time = time.ticks_ms()
        while time.ticks_ms() - 1000 < start_time:
            uart.readinto(buffer)
            if buffer[0] == CONFIRMATION_RECEIVE_CODE:
                # connection confirmed and begin sending message
                confirmed = True
                break
            elif buffer[0] == CONFIRMATION_RECEIVE_TEST_CODE:
                print("got test code")
                confirmed = True
                break
    return buffer[0]

def process_image() -> str:
    # image processing
    img = sensor.snapshot()

    blobs = img.find_blobs([(60, 100, -8, 8, -8, 8)])
    for blob in blobs:
        if blob.pixels() > 150:
            img.draw_rectangle(blob.rect(), color=(0, 255, 0))
    if len(blobs) == 0:
        return NO_IMAGE

    img.save(filepath, quality=90)
    return filepath

def label_image(labels, net):
    start_time = time.ticks_ms()
    img_found = False
    while start_time - 2 < time.ticks_ms():
        img = sensor.snapshot()
        for obj in net.classify(img, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
            predictions_list = list(zip(labels, obj.output()))
            for t in predictions_list:
                if t[1] >= 0.7:
                    img.draw_rectangle(obj.rect())
                    img.draw_string(0, 0, t[0])
                    img.save(filepath, quality=90)
                    img_found = True
        if img_found:
            break
    return filepath


def send_image(image_filepath) -> None:
    # send packets and wait for ack after each packet
    # gets stat.ST_SIZE
    global buffer
    filesize = os.stat(image_filepath)[6]
    packet_len = 500
    pointer = 0
    while (pointer < filesize):
        sleeping = True
        while (sleeping):
            uart.readinto(buffer)
            if buffer[0] == PACKET_REQ:
                sleeping = False

        else:
            with open(image_filepath, "rb") as fd:
                fd.seek(pointer)
                data = fd.read(packet_len - 1)
            packet = bytearray(len(data) + 1)

            if filesize < pointer + packet_len:
                # last packet
                packet[0] = IMAGE_END
            elif pointer == 0:
                # first packet
                packet[0] = IMAGE_START
            else:
                # mid packet
                packet[0] = IMAGE_MID
            packet[1:] = data
            uart.write(packet)
        # wait for confirmation
        confirmed = False
        s_time = time.ticks_ms()
        buffer = bytearray(1)
        while not confirmed:
            if time.ticks_ms() - 10000 > s_time:
                break
            if uart.any():
                uart.readinto(buffer)
                if buffer[0] == IMAGE_CONF:
                    pointer += (packet_len - 1)
                    confirmed = True
                    time.sleep(0.02)

def send_flag(flag):
    confirmed = False
    while not confirmed:
        buffer[0] = flag
        uart.write(buffer)
        start_time = time.ticks_ms()
        while time.ticks_ms() - 1000 < start_time:
            uart.readinto(buffer)
            if buffer[0] == IMAGE_CONF:
                # connection confirmed and begin sending message
                confirmed = True


if __name__ == '__main__':
    try:
        if "images" not in os.listdir():
            os.mkdir("images")
    except Exception as e:
        print(f"could not create images directory: {e}")

    net = None
    labels = None

    try:
        # Load built in model
        labels, net = tf.load_builtin_model('trained')
    except Exception as e:
        raise Exception(e)

    # check that the UART connection is good
    req = check_connection()

    if req == CONFIRMATION_RECEIVE_CODE:
        # take, process, and save an image
        img_filepath = label_image(labels, net)

        # send the current image
        if img_filepath == NO_IMAGE:
            send_flag(NO_IMAGE)
        else:
            send_image(img_filepath)
    elif req == CONFIRMATION_RECEIVE_TEST_CODE:
        print("sending test image")
        send_image(test_filepath)
