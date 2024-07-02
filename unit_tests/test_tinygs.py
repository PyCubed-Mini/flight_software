import sys
import unittest
from unittest import IsolatedAsyncioTestCase
import time
from numpy import array
import base64
import struct

sys.path.insert(0, './drivers/emulation/lib')
sys.path.insert(0, './drivers/emulation/')
sys.path.insert(0, './applications/flight')
sys.path.insert(0, './applications/flight/lib')
sys.path.insert(0, './frame/')
sys.path.insert(0, 'unit_tests/TinyGS-decoder/')

import radio_utils.headers as headers
from pycubed import cubesat
from radio_test_utils import init_radio_task_for_testing
from state_machine import state_machine
from Tasks.telemetry import task as telemetry
from pocketqubeDecoder import main as decoder
from lib.logs import beacon_packet, beacon_format

class TelemetryTaskTest(IsolatedAsyncioTestCase):
    async def test_beacon(self):
        '''Run telemetry main task and then have it decoded'''

        mag_in = array([4.0, 3.0, 1.0])
        gyro_in = array([-42.0, 0.1, 7.0])
        accel_in = array([-2.0, 0.1, 17.8])

        cpu_temp_in = 77
        imu_temp_in = 22

        boot_count_in = 453
        f_contact_in = True
        f_burn_in = False
        error_count_in = 13
        vbatt_in = 3.45

        rssi_in = -88.8
        fei_in = -987.0

        state_machine.states = [1, 2, 3, 4]
        state_machine.state = 2

        cubesat.f_contact = f_contact_in
        cubesat.f_burn = f_burn_in
        cubesat.c_software_error = error_count_in

        cubesat.c_boot = boot_count_in
        cubesat.LOW_VOLTAGE = vbatt_in
        cubesat.randomize_voltage = False

        cubesat._mag = mag_in
        cubesat._gyro = gyro_in
        cubesat._accel = accel_in
        cubesat._cpu_temp = cpu_temp_in
        cubesat._imu_temperature = imu_temp_in

        cubesat.radio._last_rssi = rssi_in
        cubesat.radio._frequency_error = fei_in

        packet = beacon_packet()

        actual_packet = bytearray(len(packet) + 1)
        actual_packet[0] = headers.BEACON
        actual_packet[1:] = beacon_packet()

        rt = init_radio_task_for_testing()
        tel = telemetry()

        await tel.main_task()
        await rt.main_task()

        tx_packet = cubesat.radio.test.last_tx_packet
        self.assertEqual(tx_packet, actual_packet, "Got unexpected packet")

        expected_decoded_packet = struct.unpack(beacon_format, packet)

        decoded_packet = decoder([base64.b64encode(tx_packet)])['payload']

        counter = 0
        for value in decoded_packet:
            if value == 'pad_byte': continue  # Note that python struct adds a pad byte
            self.assertAlmostEqual(decoded_packet[value], expected_decoded_packet[counter], 'Got unexpected decoding')
            counter += 1

if __name__ == '__main__':
    unittest.main()