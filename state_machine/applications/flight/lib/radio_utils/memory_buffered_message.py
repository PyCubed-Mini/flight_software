from .message import Message
from . import headers
from . import MAX_PACKET_LEN
from .hash import bsdChecksum

class MemoryBufferedMessage(Message):
    """Transmits the message PACKET_DATA_LEN bytes at a time.
    Sets special headers for the first packet, middle packets, and last packet.
    Uses the last two bytes of each packet to store a checksum.

    :param priority: The priority of the message (higher is better)
    :type priority: int
    :param str: The message to send
    :type str: str | bytes | bytearray
    """

    packet_len = MAX_PACKET_LEN
    data_len = MAX_PACKET_LEN - 3

    def __init__(self, priority, str):
        super().__init__(priority, str)
        self.cursor = 0

    def packet(self):
        payload = self.str[self.cursor:self.cursor + self.data_len]
        pkt = bytearray(len(payload) + 3)
        if len(self.str) <= self.cursor + self.data_len:  # last packet
            pkt[0] = headers.MEMORY_BUFFERED_END
        elif self.cursor == 0:
            pkt[0] = headers.MEMORY_BUFFERED_START
        else:
            pkt[0] = headers.MEMORY_BUFFERED_MID

        pkt[1:len(pkt) - 2] = payload
        pkt[len(pkt) - 2:] = bsdChecksum(payload)
        return pkt, True

    def done(self):
        return len(self.str) <= self.cursor

    def ack(self):
        self.cursor += self.data_len
