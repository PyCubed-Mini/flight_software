import time
from lib.pycubed import cubesat
try:
    import ulab.numpy as numpy
except ImportError:
    import numpy

def sweep_mag(wave_generator, coils, period, runtime, dt, amplitude_range=(-1.0, 1.0), print_data=True):
    assert amplitude_range[0] >= -1.0
    assert amplitude_range[0] <= 1.0
    assert amplitude_range[1] >= -1.0
    assert amplitude_range[1] <= 1.0
    assert amplitude_range[0] < amplitude_range[1]

    vout = [0.0, 0.0, 0.0]
    cubesat.coildriver_vout(vout)
    if print_data:
        print(f"Time,\t Coil,\t Level,\t Mag X,\t Mag Y,\t Mag Z")

    n_steps = int(runtime // dt)

    for coil_index in coils:
        for i in range(n_steps):
            t = i * dt
            half_amplitude = (amplitude_range[1] - amplitude_range[0]) / 2
            level = half_amplitude * wave_generator(t * period) + amplitude_range[0] + half_amplitude
            vout[coil_index] = level
            cubesat.coildriver_vout(vout)
            mag_reading = cubesat.magnetic
            if print_data:
                print(f"{t},\t {coil_index},\t {level},\t {mag_reading[0]},\t {mag_reading[1]},\t {mag_reading[2]}")
            time.sleep(dt)

        vout = [0.0, 0.0, 0.0]
        cubesat.coildriver_vout(vout)

def sin_generator(t):
    return numpy.sin(t * 2 * numpy.pi)

def ramp_generator(t):
    return 2.0 * (t % 1.0) - 1.0

async def run(result_dict):
    """
    """
    print("Running sine sweep\n")
    sweep_mag(sin_generator, [0, 1, 2], 1, 10, 0.01)
    print("\nSine sweep complete")

    print("Running ramp sweep\n")
    sweep_mag(ramp_generator, [0, 1, 2], 1, 10, 0.01)
    print("\nRamp sweep complete")

    result_dict["Mag_Sweep"] = ("Completed", True)
