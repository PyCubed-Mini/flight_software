from Tasks.blink import blink

from TransitionFunctions import blinkOn, blinkOff

from config import config

TaskMap = {
    'blink': blink
}

TransitionFunctionMap = {
    'BlinkOn': blinkOn,
    'BlinkOff': blinkOff
}