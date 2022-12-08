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
from shell_utils import bold, normal, red, green, yellow, blue, get_input_discrete, get_input_range


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
