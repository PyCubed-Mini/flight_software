"""
Provides individual groundstation actions such as upload a file,
wait for packet, or send a command.
"""
import board
import busio
import digitalio
from lib import pycubed_rfm9x_fsk
from lib.logs import unpack_beacon
from lib.radio_utils.disk_buffered_message import DiskBufferedMessage
from lib.radio_utils import headers
from lib.radio_utils.commands import super_secret_code
from lib.configuration import radio_configuration as rf_config
from shell_utils import bold, normal

def initialize_radio(cs, reset):
    """
    Initialize the radio - uses lib/configuration/radio_configuration to configure with defaults
    """

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    radio = pycubed_rfm9x_fsk.RFM9x(
        spi,
        cs,
        reset,
        rf_config.FREQUENCY,
        checksum=rf_config.CHECKSUM)

    # configure to match satellite
    radio.tx_power = rf_config.TX_POWER
    radio.bitrate = rf_config.BITRATE
    radio.frequency_deviation = rf_config.FREQUENCY_DEVIATION
    radio.rx_bandwidth = rf_config.RX_BANDWIDTH
    radio.preamble_length = rf_config.PREAMBLE_LENGTH
    radio.ack_delay = rf_config.ACK_DELAY
    radio.ack_wait = rf_config.ACK_WAIT
    radio.node = rf_config.GROUNDSTATION_ID
    radio.destination = rf_config.SATELLITE_ID

    return radio

def satellite_cs_reset():
    # pocketqube
    cs = digitalio.DigitalInOut(board.RF_CS)
    reset = digitalio.DigitalInOut(board.RF_RST)
    cs.switch_to_output(value=True)
    reset.switch_to_output(value=True)

    radio_DIO0 = digitalio.DigitalInOut(board.RF_IO0)
    radio_DIO0.switch_to_input()
    radio_DIO1 = digitalio.DigitalInOut(board.RF_IO1)
    radio_DIO1.switch_to_input()

    return cs, reset

def feather_cs_reset():
    # feather
    cs = digitalio.DigitalInOut(board.D5)
    reset = digitalio.DigitalInOut(board.D6)
    cs.switch_to_output(value=True)
    reset.switch_to_output(value=True)

    return cs, reset

def pi_cs_reset():
    cs = digitalio.DigitalInOut(board.CE1)
    reset = digitalio.DigitalInOut(board.D25)

    return cs, reset

async def send_command(radio, command_bytes, args, will_respond, debug=False):
    success = False
    response = None
    msg = bytes([headers.COMMAND]) + super_secret_code + command_bytes + bytes(args, 'utf-8')
    if await radio.send_with_ack(msg, debug=debug):
        if debug:
            print('Successfully sent command')
        if will_respond:
            if debug:
                print('Waiting for response')
            type, response = await wait_for_message(radio)
        success = True
    else:
        if debug:
            print('Failed to send command')
        success = False
    return success, response

def download_file():
    pass

async def upload_file(radio, path):
    msg = DiskBufferedMessage(0, path)
    while True:
        packet, with_ack = msg.packet()

        debug_packet = str(packet)[:20] + "...." if len(packet) > 23 else packet
        print(f"Sending packet: {debug_packet}, with_ack: {with_ack}")

        if with_ack:
            if await radio.send_with_ack(packet, debug=True):
                print('ack')
                msg.ack()
            else:
                print('no ack')
                msg.no_ack()
        else:
            await radio.send(packet, keep_listening=True)

        if msg.done():
            break


async def receive(rfm9x, with_ack=True):
    """Recieve a packet.  Returns None if no packet was received.
    Otherwise returns (header, payload)"""
    packet = await rfm9x.receive(with_ack=with_ack, with_header=True, debug=True)
    if packet is None:
        return None
    return packet[0:6], packet[6:]


def print_res(res):
    if res is None:
        print("No packet received")
    else:
        header, payload = res
        print("Received (raw header):", [hex(x) for x in header])
        if header[5] == headers.DEFAULT:
            print('Received beacon')
        else:
            packet_text = str(payload, "utf-8")
            print(packet_text)


class _data:

    def __init__(self):
        self.msg = bytes([])
        self.msg_last = bytes([])
        self.cmsg = bytes([])
        self.cmsg_last = bytes([])

async def wait_for_message(radio):
    data = _data()

    while True:
        res = await receive(radio)
        if res is None:
            continue
        header, payload = res

        oh = header[5]
        if oh == headers.DEFAULT or oh == headers.BEACON:
            return oh, payload
        elif oh == headers.MEMORY_BUFFERED_START or oh == headers.MEMORY_BUFFERED_MID or oh == headers.MEMORY_BUFFERED_END:
            handle_memory_buffered(oh, data, payload)
            if oh == headers.MEMORY_BUFFERED_END:
                return headers.MEMORY_BUFFERED_START, data.msg

        elif oh == headers.DISK_BUFFERED_START or oh == headers.DISK_BUFFERED_MID or oh == headers.DISK_BUFFERED_END:
            handle_disk_buffered(oh, data, payload)
            if oh == headers.DISK_BUFFERED_END:
                return headers.DISK_BUFFERED_START, data.cmsg

def print_message(header, message):
    if header == headers.DEFAULT:
        print(f"Default: {message}")
    elif header == headers.BEACON:
        print_beacon(message)
    elif header == headers.MEMORY_BUFFERED_START or header == headers.DISK_BUFFERED_START:
        print(f"Buffered:\n\t{message}")
    else:
        print(f"Unknown: {message}")

def print_beacon(beacon):
    beacon_dict = unpack_beacon(beacon)
    print(f"\n{bold}Beacon:{normal}")
    for bk in beacon_dict:
        bv = beacon_dict[bk]
        print(f"\t{bv['str']} = {bv['value']}")


async def read_loop(radio):

    while True:
        print_message(wait_for_message(radio))

def handle_memory_buffered(header, data, payload):
    if header == headers.MEMORY_BUFFERED_START:
        data.msg_last = payload
        data.msg = payload
    else:
        if payload != data.msg_last:
            data.msg += payload
        else:
            data.debug('Repeated payload')

    if header == headers.MEMORY_BUFFERED_END:
        data.msg_last = bytes([])
        data.msg = str(data.msg, 'utf-8')
        print(data.msg)


def handle_disk_buffered(header, data, response):
    if header == headers.DISK_BUFFERED_START:
        data.cmsg = response
        data.cmsg_last = response
    else:
        if response != data.cmsg_last:
            data.cmsg += response
        else:
            data.debug('Repeated payload')
        data.cmsg_last = response

    if header == headers.DISK_BUFFERED_END:
        data.cmsg_last = bytes([])
        data.cmsg = str(data.cmsg, 'utf-8')
        print('Recieved disk buffered message')
        print(data.cmsg)
