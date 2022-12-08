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
from lib import pycubed_rfm9x_fsk
from lib import radio_defaults
from shell_utils import bold, normal, red, green, yellow, blue, get_input_discrete, manually_configure_radio, print_radio_configuration


print(f"\n{bold}{yellow}PyCubed-Mini Groundstation Shell{normal}\n")

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

# Initialze radio
radio = pycubed_rfm9x_fsk.RFM9x(
    spi,
    CS,
    RESET,
    radio_defaults.FREQUENCY,
    checksum=radio_defaults.CHECKSUM)

# configure to match satellite
radio.tx_power = radio_defaults.TX_POWER
radio.bitrate = radio_defaults.BITRATE
radio.frequency_deviation = radio_defaults.FREQUENCY_DEVIATION
radio.rx_bandwidth = radio_defaults.RX_BANDWIDTH
radio.preamble_length = radio_defaults.PREAMBLE_LENGTH
radio.ack_delay = radio_defaults.ACK_DELAY
radio.ack_wait = radio_defaults.ACK_WAIT
radio.node = radio_defaults.GROUNDSTATION_ID
radio.destination = radio_defaults.SATELLITE_ID

print_radio_configuration(radio)

if "y" == get_input_discrete(
        f"Change radio parameters? {bold}(y/N){normal}", ["", "y", "n"]):
    manually_configure_radio(radio)
    print_radio_configuration(radio)

prompt_options = {"Receive loop": ("r", "receive"),
                  "Upload file": ("u", "upload"),
                  "Send command": ("c", "command"),
                  "Help": ("h", "print_help"),
                  "Quit": ("q", "quit")}

def print_help():
    print(f"\n{yellow}Groundstation shell help:{normal}")
    for po in prompt_options:
        print(f"{bold}{po}{normal}: {prompt_options[po]}")


print_help()

while True:
    flattend_prompt_options = list(sum(prompt_options.values(), ()))
    choice = get_input_discrete("Choose an action", flattend_prompt_options)
    if choice in prompt_options["Receive loop"]:
        read_loop(radio)
    elif choice in prompt_options["Upload file"]:
        path = input('path=')
        msg = ChunkMessage(0, path)
        while True:
            packet, with_ack = msg.packet()

            debug_packet = str(packet)[:20] + "...." if len(packet) > 23 else packet
            print(f"Sending packet: {debug_packet}, with_ack: {with_ack}")

            if with_ack:
                if radio.send_with_ack(packet, debug=True):
                    print('ack')
                    msg.ack()
                else:
                    print('no ack')
                    msg.no_ack()
            else:
                radio.send(packet, keep_listening=True)

            if msg.done():
                break
    elif choice in prompt_options["Send command"]:
        print(commands.keys())
        comand_bytes, will_respond = commands[input('command=')]
        args = input('arguments=')
        msg = bytes([headers.COMMAND]) + config.secret_code + comand_bytes + bytes(args, 'utf-8')
        while not radio.send_with_ack(msg, debug=True):
            print('Failed to send command')
            pass
        print('Successfully sent command')
        if will_respond:
            read_loop(radio)
    elif choice in prompt_options["Help"]:
        print_help()
    elif choice in prompt_options["Quit"]:
        break
