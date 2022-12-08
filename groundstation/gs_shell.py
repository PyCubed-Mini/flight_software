"""
Provides a basic shell-like interface to send and receive data from the satellite
"""
import board
import busio
import digitalio
import config
from utils import read_loop
import radio_utils.commands as commands
from radio_utils.disk_buffered_message import DiskBufferedMessage
from radio_utils import headers

from lib.pycubed_rfm9x_fsk import RFM9x

# print formatters
bold = '\033[1m'
normal = '\033[0m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'


def get_input_discrete(prompt_str, choice_values):
    print(prompt_str)
    choice = None

    choice_values_str = "("
    for i, _ in enumerate(choice_values):
        choice_values_str += f"{choice_values[i]}"
        if i < len(choice_values) - 1:
            choice_values_str += ", "
    choice_values_str += ")"

    choice_values = [cv.lower() for cv in choice_values]

    while choice not in choice_values:
        choice = input(f"{choice_values_str} ~> ").lower()
    return choice


def set_param_from_input_discrete(param, prompt_str, choice_values, allow_default=False, type=int):

    # add "enter" as a choice
    choice_values = [""] + choice_values if allow_default else choice_values
    prompt_str = prompt_str + \
        " (enter to skip):" if allow_default else prompt_str

    choice = get_input_discrete(prompt_str, choice_values)

    if choice == "":
        return param
    else:
        return type(choice)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_input_range(prompt_str, choice_range):
    print(prompt_str)
    choice = None

    choice_range_str = f"({choice_range[0]} - {choice_range[1]})"

    while True:
        choice = input(f"{choice_range_str} ~> ").lower()
        if choice == "":
            break

        if not is_number(choice):
            continue

        if float(choice) >= choice_range[0] and float(choice) <= choice_range[1]:
            break
    return choice


def set_param_from_input_range(param, prompt_str, choice_range, allow_default=False):

    # add "enter" as a choice
    prompt_str = prompt_str + \
        " (enter to skip):" if allow_default else prompt_str

    choice = get_input_range(prompt_str, choice_range)

    if choice == "":
        return param
    else:
        return float(choice)


print(f"\n{bold}{yellow}Radio GS Terminal{normal}\n")

board_str = get_input_discrete(
    f"Select the board {bold}(s){normal}atellite, {bold}(f){normal}eather, {bold}(r){normal}aspberry pi",
    ["s", "f", "r"]
)

if board_str == "s":
    # pocketqube
    CS = digitalio.DigitalInOut(board.RF_CS)
    RESET = digitalio.DigitalInOut(board.RF_RST)
    CS.switch_to_output(value=True)
    RESET.switch_to_output(value=True)

    radio_DIO0 = digitalio.DigitalInOut(board.RF_IO0)
    radio_DIO0.switch_to_input()
    radio_DIO1 = digitalio.DigitalInOut(board.RF_IO1)
    radio_DIO1.switch_to_input()

    print(f"{bold}{green}Satellite{normal} selected")
elif board_str == "f":
    # feather
    CS = digitalio.DigitalInOut(board.D5)
    RESET = digitalio.DigitalInOut(board.D6)
    CS.switch_to_output(value=True)
    RESET.switch_to_output(value=True)

    print(f"{bold}{green}Feather{normal} selected")
else:  # board_str == "r"
    # raspberry pi
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)
    print(f"{bold}{green}Raspberry Pi{normal} selected")

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
RADIO_FREQ_MHZ = 433.0
rfm9x = RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, checksum=True)

# configure for FSK
rfm9x.tx_power = 23
rfm9x.bitrate = 2400
rfm9x.frequency_deviation = 10000
rfm9x.rx_bandwidth = 25.0
rfm9x.preamble_length = 16
rfm9x.ack_delay = 1.0
rfm9x.ack_wait = 5

# set node/destination
rfm9x.node = 0xBA
rfm9x.destination = 0xAB

while True:
    prompt = input('~>')
    if prompt == 'rl' or prompt == 'read_loop':  # Recieve on a loop
        read_loop(rfm9x)
    elif prompt == 'uf' or prompt == 'upload_file':
        path = input('path=')
        msg = ChunkMessage(0, path)
        while True:
            packet, with_ack = msg.packet()

            debug_packet = str(packet)[:20] + "...." if len(packet) > 23 else packet
            print(f"Sending packet: {debug_packet}, with_ack: {with_ack}")

            if with_ack:
                if rfm9x.send_with_ack(packet, debug=True):
                    print('ack')
                    msg.ack()
                else:
                    print('no ack')
                    msg.no_ack()
            else:
                rfm9x.send(packet, keep_listening=True)

            if msg.done():
                break
    elif prompt == 'c' or prompt == 'command':  # Transmit particular command
        print(commands.keys())
        comand_bytes, will_respond = commands[input('command=')]
        args = input('arguments=')
        msg = bytes([headers.COMMAND]) + config.secret_code + comand_bytes + bytes(args, 'utf-8')
        while not rfm9x.send_with_ack(msg, debug=True):
            print('Failed to send command')
            pass
        print('Successfully sent command')
        if will_respond:
            read_loop(rfm9x)
    elif prompt == 'h' or prompt == 'help':
        print('rl: read_loop')
        print('uf: upload_file')
        print('c: command')
        print('h: help')
