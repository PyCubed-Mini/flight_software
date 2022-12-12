import unittest
import sys
from numpy import testing, array

sys.path.insert(0, './state_machine/drivers/emulation')
sys.path.insert(0, './state_machine/drivers/emulation/lib')
sys.path.insert(0, './state_machine/applications/flight')
sys.path.insert(0, './state_machine/frame')

from lib.logs import beacon_packet, unpack_beacon
from pycubed import cubesat
from state_machine import state_machine

class TestLogs(unittest.TestCase):

    def test(self):

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

        cubesat.f_contact = f_contact_in
        cubesat.f_burn = f_burn_in
        cubesat.c_state_err = error_count_in

        cubesat.c_boot = boot_count_in
        cubesat.LOW_VOLTAGE = vbatt_in
        cubesat.randomize_voltage = False

        cubesat._mag = mag_in
        cubesat._gyro = gyro_in
        cubesat._cpu_temp = cpu_temp_in
        cubesat._imu_temperature = imu_temp_in

        cubesat.radio._last_rssi = rssi_in
        cubesat.radio._frequency_error = fei_in

        pkt = beacon_packet()

        unpacked = unpack_beacon(pkt)

        self.assertEqual(state_in, unpacked["state_index"])
        self.assertEqual(f_contact_in, unpacked["contact_flag"])
        self.assertEqual(f_burn_in, unpacked["burn_flag"])
        self.assertEqual(error_count_in, unpacked["software_error_count"])
        self.assertEqual(boot_count_in, unpacked["boot_count"])
        self.assertAlmostEqual(vbatt_in + 0.01, unpacked["battery_voltage"], places=5)
        self.assertAlmostEqual(cpu_temp_in, unpacked["cpu_temperature_C"], places=5)
        self.assertAlmostEqual(imu_temp_in, unpacked["imu_temperature_C"], places=5)
        self.assertAlmostEqual(rssi_in, unpacked["RSSI_dB"], places=5)
        self.assertAlmostEqual(fei_in, unpacked["FEI_Hz"], places=5)
        testing.assert_array_almost_equal(gyro_in, unpacked["gyro"])
        testing.assert_array_almost_equal(mag_in, unpacked["mag"])
