"""
A simple state machine that moves between turning an LED on and then turning it off.
11/29/23

"""

config = {
    "BlinkOn": {
        "Tasks": {
            "Blink": {
                "Interval": 3,
                "Priority": 1,
                "ScheduleLater": False
            }
        },
        "StepsTo": [
            "BlinkOff"
        ],
        "EnterFunctions": [
            "BlinkOn"
        ],
        "ExitFunctions": [
            "BlinkOff"
        ]
    },
    "BlinkOff": {
        "Tasks": {
            "Blink": {
                "Interval": 3,
                "Priority": 1,
                "ScheduleLater": False
            }
        },
        "StepsTo": [
            "BlinkOn"
        ]
    }
}

initial = "BlinkOn"