# Transmit "Hello World" beacon

import time

import files
import logs
from pycubed import cubesat
from radio_utils import headers
from radio_utils.message import Message
from radio_utils.transmission_queue import transmission_queue as tq
from Tasks.log import LogTask as Task


class task(Task):
    name = 'beacon'
    color = 'teal'

    async def main_task(self):
        """
        Pushes a beacon packet onto the transmission queue.
        """
        if not cubesat.sdcard:
            return

        try:
            self.write_telemetry()
        except Exception:
            boot = cubesat.c_boot
            files.mkdirp(f'/sd/logs/telemetry/{boot:05}')
            self.write_telemetry()

    def write_telemetry(self):
        if cubesat.rtc:
            t = cubesat.rtc.datetime
        else:
            t = time.localtime()
        hour_stamp = f'{t.tm_year:04}.{t.tm_mon:02}.{t.tm_mday:02}.{t.tm_hour:02}'
        boot = cubesat.c_boot
        current_file = f"/sd/logs/telemetry/{boot:05}/{hour_stamp}"
        telemetry_packet = logs.telemetry_packet(t)
        self.downlink_beacon()
        file = open(current_file, "ab+")
        file.write(telemetry_packet)
        file.close()

    def downlink_beacon(self):
        packet = logs.beacon_packet()
        tq.push(Message(10, packet, header=headers.BEACON, with_ack=False))
        self.debug("beacon added to transmission queue")
