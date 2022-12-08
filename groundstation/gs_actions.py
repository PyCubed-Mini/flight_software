"""
Provides individual groundstation actions such as upload a file,
wait for packet, or send a command.
"""
from radio_utils.disk_buffered_message import DiskBufferedMessage
from radio_utils import headers
from radio_utils.commands import super_secret_code

def initialize_radio():
    pass

def setup_board():
    pass

def wait_for_message(radio):
    pass

def send_command(radio, command_bytes, args, will_respond):
    msg = bytes([headers.COMMAND]) + super_secret_code + command_bytes + bytes(args, 'utf-8')
    if radio.send_with_ack(msg, debug=True):
        print('Successfully sent command')
        if will_respond:
            print('Waiting for response')
            wait_for_message(radio)
    else:
        print('Failed to send command')

def download_file():
    pass

def upload_file(radio, path):
    msg = DiskBufferedMessage(0, path)
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
