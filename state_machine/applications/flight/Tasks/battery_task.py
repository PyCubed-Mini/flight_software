from lib.template_task import Task
from lib.pycubed import cubesat


class task(Task):
    name = 'vbatt'
    color = 'orange'

    timeout = 60 * 60  # 60 min

    async def main_task(self):
        vbatt = cubesat.battery_voltage()
        if cubesat.state_machine.state == 'LowPower':
            if vbatt >= cubesat.vlowbatt:
                self.debug(f'{vbatt:.1f}V ≥ {cubesat.vlowbatt:.1f}V')
                self.debug('sufficient battery detected, switching out of low power mode', 2)
                cubesat.state_machine.switch_to('Normal')
            else:
                self.debug(f'{vbatt:.1f}V < {cubesat.vlowbatt:.1f}V')
        else:
            if vbatt < cubesat.vlowbatt:
                self.debug(f'{vbatt:.1f}V < {cubesat.vlowbatt:.1f}V')
                self.debug('low battery detected!', 2)
                # switch to low power state
                cubesat.state_machine.switch_to('LowPower')
            else:
                self.debug(f'{vbatt:.1f}V ≥ {cubesat.vlowbatt:.1f}V')
