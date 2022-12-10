from pycubed import cubesat
import struct
try:
    from ulab.numpy import array
except ImportError:
    from numpy import array


beacon_format = 'H' + 'f' * 11  # 1 short + 11 floats

def beacon_packet():
    """Creates a beacon packet containing the: boot count, battery voltage,
    CPU temperature, IMU temperature, gyro reading, mag reading,
    radio signal strength (RSSI), radio frequency error (FEI).

    This data is packed into a c struct using `struct.pack`.
    """

    boot_count = cubesat.c_boot
    vbatt = cubesat.battery_voltage
    cpu_temp = cubesat.temperature_cpu
    imu_temp = cubesat.temperature_imu
    gyro = cubesat.gyro
    mag = cubesat.magnetic
    rssi = cubesat.radio.last_rssi
    fei = cubesat.radio.frequency_error
    return struct.pack(beacon_format,
                       boot_count, vbatt,
                       cpu_temp, imu_temp,
                       gyro[0], gyro[1], gyro[2],
                       mag[0], mag[1], mag[2],
                       rssi, fei)

def unpack_beacon(bytes):
    """Unpacks the fields from the beacon packet packed by `beacon_packet`
    """

    (boot_count, vbatt,
     cpu_temp, imu_temp,
     gyro0, gyro1, gyro2,
     mag0, mag1, mag2,
     rssi, fei) = struct.unpack(beacon_format, bytes)

    gyro = array([gyro0, gyro1, gyro2])
    mag = array([mag0, mag1, mag2])

    return boot_count, vbatt, cpu_temp, imu_temp, gyro, mag, rssi, fei
