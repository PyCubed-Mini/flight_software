from Tasks.blink import blink

from TransitionFunctions import announcer

from config import config

TaskMap = {
    'blink': blink
}

TransitionFunctionMap = {
    'Announcer': announcer
}