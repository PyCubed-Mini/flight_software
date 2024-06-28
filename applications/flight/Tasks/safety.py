from Tasks.log import LogTask as Task
from pycubed import cubesat
from state_machine import state_machine
from lib.alerts import alerts


class task(Task):
    name = 'safety'
    color = 'orange'

    timeout = 60 * 60  # 60 min

    def debug_status(self, vbatt, temp, curr):
        self.debug(f'Voltage: {vbatt:.2f}V | Temp: {temp:.2f}°C | Current: {curr:.2f}', log=True)

    def safe_mode(self, vbatt, temp, curr):
        # Needs to be done here, and not in transition function due to #306
        cubesat.enable_low_power()
        # margins added to prevent jittering between states
        if vbatt < cubesat.LOW_VOLTAGE + 0.1:
            self.debug(f'Voltage too low ({vbatt:.2f}V < {cubesat.LOW_VOLTAGE + 0.1:.2f}V)', log=True)
            alerts.set(self.debug, 'voltage_low')
        elif temp >= cubesat.HIGH_TEMP - 1:
            self.debug(f'Temp too high ({temp:.2f}°C >= {cubesat.HIGH_TEMP - 1:.2f}°C)', log=True)
            alerts.set(self.debug, 'temp_high')
        else:
            self.debug_status(vbatt, temp, curr)
            self.debug(
                f'Safe operating conditions reached, switching back to {state_machine.previous_state} mode', log=True)
            state_machine.switch_to(state_machine.previous_state)

    def other_modes(self, vbatt, temp, curr):
        if vbatt < cubesat.LOW_VOLTAGE:
            self.debug(f'Voltage too low ({vbatt:.2f}V < {cubesat.LOW_VOLTAGE:.2f}V) switch to safe mode', log=True)
            alerts.set(self.debug, 'voltage_low')
            state_machine.switch_to('Safe')
        if temp > cubesat.HIGH_TEMP:
            self.debug(f'Temp too high ({temp:.2f}°C > {cubesat.HIGH_TEMP:.2f}°C) switching to safe mode', log=True)
            alerts.set(self.debug, 'temp_high')
            state_machine.switch_to('Safe')
        else:
            self.debug_status(vbatt, temp, curr)
            alerts.clear(self.debug, 'temp_high')
            alerts.clear(self.debug, 'voltage_low')

    async def main_task(self):
        """
        If the voltage is too low or the temp is to high, switch to safe mode.
        If the voltage is high enough and the temp is low enough, switch to normal mode.
        """
        vbatt = cubesat.battery_voltage
        temp = cubesat.temperature_cpu
        curr = cubesat.battery_current
        if state_machine.state == 'Safe':
            self.safe_mode(vbatt, temp, curr)
        else:
            self.other_modes(vbatt, temp, curr)
