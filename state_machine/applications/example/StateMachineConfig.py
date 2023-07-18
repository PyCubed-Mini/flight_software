from Tasks.battery import task as battery
from Tasks.time import task as time
from Tasks.every_5_seconds import task as every5
from Tasks.transition import task as transition

from TransitionFunctions import announcer

from config import config  # noqa: F401

TaskMap = {
    'Battery': battery,
    'Transition': transition,
    'Time': time,
    'Every5Seconds': every5,
}

TransitionFunctionMap = {
    'Announcer': announcer
}
