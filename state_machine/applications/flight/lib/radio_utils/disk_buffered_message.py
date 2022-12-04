from .message import Message
from . import headers
from . import MAX_PACKET_LEN
import os
from .hash import bsdChecksum

class DiskBufferedMessage(Message):
    """Transmits the message PACKET_DATA_LEN bytes at a time.
    Sets special headers for the first packet, middle packets, and last packet.
    Reads from a file one chunk at a time.
    Uses the last two bytes of each packet to store a checksum.

    :param priority: The priority of the message (higher is better)
    :type priority: int
    :param path: The path to the file containing the message to send
    :type str: str | bytes | bytearray
    """

    packet_len = MAX_PACKET_LEN
    data_len = MAX_PACKET_LEN - 3

    def __init__(self, priority, path):
        self.cursor = 0
        self.priority = priority
        self.path = path
        self.msg_len = os.stat(path)[6]

    def packet(self):
        """Reads the next chunk of data from sd, and returns this is a packet.
        Always requests an ack."""
        try:
            with open(self.path, "rb") as f:
                f.seek(self.cursor)
                payload = f.read(self.data_len)
        except Exception as e:
            print(f'Error reading file {self.path}: {e}')
        pkt = bytearray(len(payload) + 3)
        if self.msg_len <= self.cursor + self.data_len:  # last packet
            pkt[0] = headers.DISK_BUFFERED_END
        elif self.cursor == 0:
            pkt[0] = headers.DISK_BUFFERED_START
        else:
            pkt[0] = headers.DISK_BUFFERED_MID

        pkt[1:len(pkt) - 2] = payload
        pkt[len(pkt) - 2:] = bsdChecksum(payload)
        return pkt, True

    def done(self):
        return self.msg_len <= self.cursor

    def ack(self):
        self.cursor += self.data_len

    def __repr__(self) -> str:
        return f'<Disk Buffer: {self.path}>'
