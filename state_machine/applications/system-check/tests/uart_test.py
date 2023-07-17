from lib.pycubed import cubesat
import time

async def run(result_dict):
    cubesat.cam_pin.value = True
    confirmed = False
    st = time.monotonic()
    buffer = bytearray(1)
    while not confirmed:
        if time.monotonic() - 10 > st:
            result_dict["UART"] = ("timeout", False)
            break

        cubesat.uart.readinto(buffer)
        if buffer[0] == 0xAA:
            result_dict["UART"] = ("camera is on and running correct script", True)
            confirmed = True
        elif buffer[0] != 0xAA and buffer != 0x00:
            result_dict["UART"] = ("camera is on but may be running the wrong script", False)

    cubesat.cam_pin.value = False
