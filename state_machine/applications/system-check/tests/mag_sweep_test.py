import time
import files
from lib.pycubed import cubesat
try:
    import ulab.numpy as numpy
except ImportError:
    import numpy

def human_time_stamp(t):
    """Returns a human readable time stamp in the format: 'boot_year.month.day_hour:min'
    Gets the time from the RTC.

    :param t: The time to format
    :type t: time.struct_time"""
    boot = cubesat.c_boot
    return f'{boot:05}_{t.tm_year:04}.{t.tm_mon:02}.{t.tm_mday:02}_{t.tm_hour:02}.{t.tm_min:02}.{t.tm_sec:02}'

def sweep_mag(wave_generator, coils, period, runtime, dt, amplitude=1.0, offset=0.0, print_data=True, logfile=""):
    vout = [0.0, 0.0, 0.0]
    cubesat.coildriver_vout(vout)
    if not logfile == "":
        logfile += human_time_stamp(cubesat.rtc.datetime) + ".csv"
        print(f"Logging to {logfile}")
        files.mkdirp(logfile[0:logfile.rfind("/")])  # make directories up to file name
        log_fd = open(logfile, 'a')
        log_fd.write(f"Time, Coil, Level, Mag X, Mag Y, Mag Z\n")
    if print_data:
        print(f"Time,\t Coil,\t Level,\t Mag X,\t Mag Y,\t Mag Z")

    n_steps = int(runtime // dt)

    for coil_index in coils:
        for i in range(n_steps):
            t = i * dt
            level = amplitude * wave_generator(t * period) + offset
            vout[coil_index] = level
            cubesat.coildriver_vout(vout)
            if print_data:
                mag_reading = cubesat.magnetic
                print(f"{t},\t {coil_index},\t {level},\t {mag_reading[0]},\t {mag_reading[1]},\t {mag_reading[2]}")
            if not logfile == "":
                tstart = time.monotonic()
                while time.monotonic() - tstart < dt:
                    mag_reading = cubesat.magnetic
                    log_fd.write(f"{time.monotonic()}, {coil_index}, {level}, {mag_reading[0]}, {mag_reading[1]}, {mag_reading[2]}\n")
            else:
                time.sleep(dt)

        vout = [0.0, 0.0, 0.0]
        cubesat.coildriver_vout(vout)

    if not logfile == "":
        log_fd.close()

def sin_generator(t):
    return numpy.sin(t * 2 * numpy.pi)

def ramp_generator(t):
    return 2.0 * (t % 1.0) - 1.0

def pulse_generator(t, duty=0.1):
    if (t % 1.0) <= duty:
        return 1.0
    else:
        return 0.0

async def run(result_dict):
    """
    """
    # print("Running sine sweep\n")
    # sweep_mag(sin_generator, [0, 1, 2], 1, 10, 0.01)
    # print("\nSine sweep complete")

    # print("Running ramp sweep\n")
    # sweep_mag(ramp_generator, [0, 1, 2], 1, 10, 0.01)
    # print("\nRamp sweep complete")

    print("Running pulse sweep\n")
    sweep_mag(lambda t: pulse_generator(t, duty=0.1), [0, 1, 2], 1, 5.0, 0.01,
              amplitude=1.0, offset=0.0, print_data=False, logfile="/sd/tests/mag_sweep/pulse_")
    print("\nPulse sweep complete")

    result_dict["Mag_Sweep"] = ("Completed", True)
