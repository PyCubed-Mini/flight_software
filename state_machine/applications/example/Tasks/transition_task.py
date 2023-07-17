from lib.template_task import Task
from state_machine import state_machine


class task(Task):

    async def main_task(self):
        if state_machine.state == 'Normal':
            print('Switching to Special mode')
            state_machine.switch_to('Special')
        else:
            print('Switching to Normal mode')
            state_machine.switch_to('Normal')
