# check for low battery condition

from lib.template import Task
from lib.pycubed import cubesat


class task(Task):

    async def main_task(self):
        # Tasks have access to the cubesat object, and can get readings like battery voltage
        print(f'Current battery voltage: {cubesat.battery_voltage}')
