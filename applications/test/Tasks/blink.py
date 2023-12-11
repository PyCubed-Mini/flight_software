from lib.template_task import Task
from lib.pycubed import cubesat

class task(Task):

    async def main_task(self):
        #Checks if the neopixel is attached
        if not cubesat.neopixel:
            self.debug("No neopixel attached!")
