"""
Simple script for doing typical groundstation operations as 
part of a day in the life test.

Only meant to run on raspberry pi.
"""
import time
import tasko
import argparse

from shell_utils import bold, normal, red, green, yellow, blue, get_input_discrete, manually_configure_radio, print_radio_configuration
# from gs_shell_tasks import *
# from gs_setup import *

parser = argparse.ArgumentParser(
    prog="ditl_groundstation.py",
    description="Simple script for doing typical groundstation" +
    "operations as part of a day in the life test.")

parser.add_argument('log_filename')
parser.add_argument('--beacon_frequency_hz', default=1.0 / 20)

args = parser.parse_args()

def human_time_stamp():
    """Returns a human readable time stamp in the format: 'year.month.day hour:min'
    Gets the local time."""
    t = time.localtime()
    return f'{t.tm_year:4}.{t.tm_mon:02}.{t.tm_mday:02}.{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}'

def log_print(str, printcolor=normal):
    """
    Timestamp, print to stdout and log str to a file
    """
    timestamp = human_time_stamp()

    print(f"[{yellow}{timestamp}{normal}]\t" +
          f"{printcolor}{str}{normal}")

    with open(args.log_filename, "a") as f:
        f.write(f"[{timestamp}]\t" +
                f"{str}" + "\n")


async def get_beacon():
    log_print(f"Requesting beacon...")
    success = True
    if success:
        beaconstr = ""
        log_print(f"Successful beacon request" + beaconstr, printcolor=green)
    else:
        log_print(f"Failed beacon request", printcolor=red)

tasko.schedule(args.beacon_frequency_hz, get_beacon, 10)
tasko.run()
