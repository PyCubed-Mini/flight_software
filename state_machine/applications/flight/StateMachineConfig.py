from Tasks.safety import task as safety
from Tasks.telemetry import task as telemetry
from Tasks.blink import task as blink
from Tasks.imu import task as imu
from Tasks.time import task as time
from Tasks.gnc import task as gnc
from Tasks.radio import task as radio
from Tasks.deployment_manager import deployment_manager
from Tasks.hw_monitor import task as hw_monitor
from TransitionFunctions import announcer, low_power_on, low_power_off
from config import config  # noqa: F401

TaskMap = {
    "Safety": safety,
    "Telemetry": telemetry,
    "Blink": blink,
    "IMU": imu,
    "Time": time,
    "GNC": gnc,
    "Radio": radio,
    "DeploymentManager": deployment_manager,
    "HwMonitor": hw_monitor,
}

TransitionFunctionMap = {
    'Announcer': announcer,
    'LowPowerOn': low_power_on,
    'LowPowerOff': low_power_off,
}
