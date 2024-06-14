import sys
import unittest
import time
from numpy import array
import base64

sys.path.insert(0, './drivers/emulation/lib')
sys.path.insert(0, './drivers/emulation/')
sys.path.insert(0, './applications/flight')
sys.path.insert(0, './applications/flight/lib')
sys.path.insert(0, './frame/')
sys.path.insert(0, 'unit_tests/TinyGS-decoder/')

from radio_driver import _Packet as Packet
import radio_utils.commands as cdh
from pycubed import cubesat
from testutils import command_data
from radio_test_utils import init_radio_task_for_testing
from state_machine import state_machine
from pocketqubeDecoder import main as decoder
from prometheusDecoder import main as new_decoder
from Tasks.log import LogTask
from lib.logs import telemetry_packet, unpack_telemetry

debug = LogTask()

# We want it to return instantly

class BeaconDecoderTest(unittest.TestCase):
    def test_beacon(self):
        '''Create a fake beacon request and then have it decoded'''

        mag_in = array([4.0, 3.0, 1.0])
        gyro_in = array([-42.0, 0.1, 7.0])

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
        state_in = state_machine.states.index(state_machine.state)

        lux_xp_in = 12.3
        lux_yp_in = 0.2
        lux_zp_in = 5.0

        lux_xn_in = 6.0
        lux_yn_in = 8.1
        lux_zn_in = 2.0

        time_in = time.localtime()
        tm_min_in = time_in.tm_min
        tm_sec_in = time_in.tm_sec

        cubesat.f_contact = f_contact_in
        cubesat.f_burn = f_burn_in
        cubesat.c_software_error = error_count_in

        cubesat.c_boot = boot_count_in
        cubesat.LOW_VOLTAGE = vbatt_in
        cubesat.randomize_voltage = False

        cubesat._mag = mag_in
        cubesat._gyro = gyro_in
        cubesat._cpu_temp = cpu_temp_in
        cubesat._imu_temperature = imu_temp_in

        cubesat.radio._last_rssi = rssi_in
        cubesat.radio._frequency_error = fei_in

        cubesat._luxp = array([lux_xp_in, lux_yp_in, lux_zp_in])
        cubesat._luxn = array([lux_xn_in, lux_yn_in, lux_zn_in])

        beacon_packet = bytearray(b'\x02') + telemetry_packet(time_in)

        debug.debug(unpack_telemetry(telemetry_packet(time_in)))

        debug.debug(len(beacon_packet))

        debug.debug(f'Packet that was sent: {beacon_packet}')

        debug.debug(new_decoder([base64.b64encode(beacon_packet)]))

if __name__ == '__main__':
    unittest.main()