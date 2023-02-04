import time
from lib.pycubed import cubesat
try:
    import ulab.numpy as numpy
except ImportError:
    import numpy

def sweep_mag(wave_generator, coil_index, period, time, dt, amplitude_range=(-1.0, 1.0), print_data=True):
    assert amplitude_range[0] > -1.0
    assert amplitude_range[0] < 1.0
    assert amplitude_range[1] > -1.0
    assert amplitude_range[1] < 1.0
    assert amplitude_range[0] < amplitude_range[1]

    vout = [0.0, 0.0, 0.0]
    cubesat.coildriver_vout(vout)
    if print_data:
        print(f"Coil,\t Level,\t Mag X,\t Mag Y,\t Mag Z")

    for t in range(time, step=dt):
        level = (amplitude_range[1] - amplitude_range[0]) * wave_generator(t * period) - amplitude_range[0]
        vout[coil_index] = level
        cubesat.coildriver_vout(vout)
        mag_reading = cubesat.magnetic()
        if print_data:
            print(f"{coil_index},\t {level},\t {mag_reading[0]},\t {mag_reading[1]},\t {mag_reading[2]}")
        time.sleep(dt)

    vout = [0.0, 0.0, 0.0]
    cubesat.coildriver_vout(vout)

def sin_generator(t):
    return numpy.sin(t * 2 * numpy.pi)

def ramp_generator(t):
    return t % 1.0

async def run(result_dict):
    """
    """
    pass
