from .message import Message
from radio_utils import PACKET_DATA_LEN
import os
# from configuration.radio_configuration import PROTOCOL
from .headers import IMAGE_END, IMAGE_MID, IMAGE_START


class ImageMessage(Message):
    """
    encodes JPEG files into packets that can be transmitted over RF
        - works for baseline DCT

    You can find out if your JPEG image uses baseline DCT by looking at the start of frame
    bytes. If they are FFC0, it is baseline otherwise it will be FFC2
    """

    headers = {
        0xFF, 0xD8, 0xC0, 0xC2, 0xC4, 0xDA, 0xDB, 0xDD, 0xFE, 0xD9
    }

    SIG = bytearray(1)
    SIG[0] = 0xFF

    SOS = bytearray(2)
    SOS[0] = 0xFF
    SOS[1] = 0xDA

    EOI = bytearray(2)
    EOI[0] = 0xFF
    EOI[1] = 0xD9

    # if PROTOCOL == "lora":
    #     packet_size = LORA_PACKET_DATA_LEN
    # elif PROTOCOL == "fsk":
    #     packet_size = FSK_PACKET_DATA_LEN

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.length = os.stat(filepath)[6]
        self.sent_packet_len = 0
        self.cursor = 0
        self.packet_size = PACKET_DATA_LEN
        self.in_scan = False
        self.found_scan = False
        self.file_err = False
        self.scan_size = ((self.packet_size - 1) // 64) * 64
        self.count = 0
        self.priority = 2

    def packet(self) -> bool:
        """
        packet 0 to n:
            header, comment, huffman tables, quantization tables.
            If even a single byte of data is lost here the entire image is done for.
            Therefore, its not really worth doing any special manipulation to the packets.
            these are sent in packets that are as large as possible
        packet j + 1 to k
            image scan

        writes this packet into the given buffer
        """
        if self.in_scan:
            """
            Should use 64 byte increments in the image scan section
            """
            try:
                with open(self.filepath, "rb") as file:
                    file.seek(self.cursor)
                    data = file.read(self.scan_size)
            except Exception as e:
                print(f"error reading from image file: {e}")
                self.file_err = True

        else:
            """
            If we are in the header bytes still
            """
            try:
                with open(self.filepath, "rb") as file:
                    file.seek(self.cursor)
                    data = file.read(self.packet_size)
            except Exception as e:
                print(f"error reading from image file: {e}")
                self.file_err = True

        self.sent_packet_len = len(data) + 1
        packet = bytearray(self.sent_packet_len)

        if self.cursor == 0:
            """start packet"""
            packet[0] = IMAGE_START
        elif self.EOI in data:
            """end packet"""
            packet[0] = IMAGE_END
        else:
            """mid packet"""
            packet[0] = IMAGE_MID
        packet[1] = self.count
        packet[2:] = data

        # update cursor and count
        self.cursor += self.sent_packet_len - 1
        self.count += 1

        # no longer using Acks for image packets
        return packet, False

    def done(self) -> bool:
        return (self.length <= self.cursor) or self.file_err

    def ack(self) -> None:
        """
        confirms that we should move to the next packet of info
        """
        if self.found_scan:
            self.in_scan = True
        # cursor moves by packet len minus the 1 byte header
        # self.cursor += self.sent_packet_len - 1
        # self.count += 1

    def __repr__(self) -> str:
        return f'<Image: {self.filepath}'
