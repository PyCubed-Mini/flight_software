from lib.template_task import Task
from pycubed import cubesat
from state_machine import state_machine


class deployment_manager(Task):
    name = 'depoloyment_manager'
    color = 'blue'

    rgb_on = False

    async def main_task(self):
        # nvm shit
        if (cubesat.f_contact):
            state_machine.switch_to('Normal')
        else:
            if await cubesat.burn(duration=15):
                self.debug('Successfully burned')
            else:
                # Consider panic mode
                self.debug('Unsuccessful burn')
