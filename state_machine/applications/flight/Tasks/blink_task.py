# Blink the RGB LED

from Tasks.log import LogTask as Task
from pycubed import cubesat
from state_machine import state_machine


class task(Task):
    name = 'blink'
    color = 'pink'

    rgb_on = False

    state_colors = [(0, 50, 50), (50, 0, 50), (0, 0, 10)]
    unknown_state_color = (30, 30, 30)

    async def main_task(self):
        """
        Switches the LED from purple to off.
        """
        if not cubesat.neopixel:
            self.debug('No neopixel attached, skipping blink task')
            return
        if self.rgb_on:
            cubesat.RGB = (0, 0, 0)
            self.rgb_on = False
        else:
            state_index = state_machine.states.index(state_machine.state)
            if state_index < len(self.state_colors):
                cubesat.RGB = self.state_colors[state_index]
            else:
                cubesat.RGB = self.unknown_state_color
            self.rgb_on = True
