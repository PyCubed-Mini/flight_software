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

        boot_count_out, vbatt_out, cpu_temp_out, imu_temp_out, gyro_out, mag_out, rssi_out, fei_out = unpack_beacon(pkt)

        self.assertEqual(boot_count_in, boot_count_out)
        self.assertAlmostEqual(vbatt_in + 0.01, vbatt_out, places=5)
        self.assertAlmostEqual(cpu_temp_in, cpu_temp_out, places=5)
        self.assertAlmostEqual(imu_temp_in, imu_temp_out, places=5)
        self.assertAlmostEqual(rssi_in, rssi_out, places=5)
        self.assertAlmostEqual(fei_in, fei_out, places=5)
        testing.assert_array_almost_equal(gyro_in, gyro_out)
        testing.assert_array_almost_equal(mag_in, mag_out)
