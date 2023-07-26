class Universe():

    def __init__(self):
        from pycubed import cubesat
        from state_machine import state_machine
        from config import initial
        state_machine.start(initial)
        self.cubesat = cubesat
        self.state_machine = state_machine

    def terminate(self):
        self.state_machine.stop_all()
