import unittest
import sys
from numpy import testing, array

sys.path.insert(0, './state_machine/drivers/emulation')
sys.path.insert(0, './state_machine/drivers/emulation/lib')
sys.path.insert(0, './state_machine/applications/flight')
sys.path.insert(0, './state_machine/frame')

from lib.logs import beacon_packet, unpack_beacon
from pycubed import cubesat

class TestLogs(unittest.TestCase):

    def test(self):

        mag_in = array([4.0, 3.0, 1.0])
        gyro_in = array([-42.0, 0.1, 7.0])

        cpu_temp_in = 77
        imu_temp_in = 22

        boot_count_in = 453
        vbatt_in = 3.45

        rssi_in = -88.8
        fei_in = -987.0

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

        self.assertEqual(boot_count_in, unpacked["boot_count"]["value"])
        self.assertAlmostEqual(vbatt_in + 0.01, unpacked["vbatt"]["value"], places=5)
        self.assertAlmostEqual(cpu_temp_in, unpacked["cpu_temp"]["value"], places=5)
        self.assertAlmostEqual(imu_temp_in, unpacked["imu_temp"]["value"], places=5)
        self.assertAlmostEqual(rssi_in, unpacked["rssi"]["value"], places=5)
        self.assertAlmostEqual(fei_in, unpacked["fei"]["value"], places=5)
        testing.assert_array_almost_equal(gyro_in, unpacked["gyro"]["value"])
        testing.assert_array_almost_equal(mag_in, unpacked["mag"]["value"])
