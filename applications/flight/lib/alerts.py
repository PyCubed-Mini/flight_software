class AlertManager:

    def __init__(self, valid_alerts):
        self.valid_alerts = valid_alerts
        self.alerts = {}

    def validate(self, alert):
        if alert not in self.valid_alerts:
            raise ValueError(f'"{alert}" is not a valid alert')

    def set(self, debug, alert):
        self.validate(alert)
        if (alert not in self.alerts) or (self.alerts[alert] == 0):
            self.alerts[alert] = 1
            debug(f'Alert "{alert}" set')

    def clear(self, debug, alert):
        self.validate(alert)
        if (alert in self.alerts) and (self.alerts[alert] == 1):
            self.alerts[alert] = 0
            debug(f'Alert "{alert}" cleared')

    def set_value(self, debug, alert, value):
        self.validate(alert)
        if (alert not in self.alerts) or (self.alerts[alert] != value):
            self.alerts[alert] = value
            if value:
                debug(f'Alert "{alert}" set')
            else:
                debug(f'Alert "{alert}" cleared')


alerts = AlertManager(
    {
        'imu_available',
        'radio_available',
        'radio_task_disabled',
        'rtc_available',
        'neopixel_available',
        'current_sensor_available',
    }
)
