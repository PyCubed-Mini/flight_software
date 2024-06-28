from Tasks.log import LogTask as Task
from radio_utils.image_queue import image_queue as iq
import files
from pycubed import cubesat
from time import monotonic, localtime
from gc import collect
from lib.alerts import alerts
from lib.image_utils import flags
import tasko
import os

# constants
CONFIRMATION_SEND_CODE = 0xAA
CONFIRMATION_RECEIVE_CODE = 0xAB
IMAGE_START = 0xAC
IMAGE_MID = 0xAD
IMAGE_END = 0xAE
IMAGE_CONF = 0xAF
PACKET_REQ = 0xB0
NO_IMAGE = 0xB1
MAX_CONF_ATTEMPTS = 3

class task(Task):
    name = 'image'
    color = 'blue'

    last_time = monotonic()
    cam_on = False
    cam_active = False
    conf_attempts = 0

    filepath = ""

    def should_activate(self):
        """
        clock that returns True every 60 seconds
        """
        if monotonic() - 60 > self.last_time:
            self.last_time = monotonic()
            return True
        return False

    async def main_task(self):
        """
        gets an image from the camera board
        """
        # image task requires sd card to get an image
        if not cubesat.camera or not cubesat.sdcard:
            alerts.clear(self.debug, 'image_queue_full')
            return
        elif iq.size() >= 5:
            alerts.set(self.debug, 'image_queue_full')
            return
        else:
            alerts.clear(self.debug, 'image_queue_full')
        collect()

        st = monotonic()
        if self.should_activate() and not self.cam_active and not self.cam_on:
            # turn the camera on
            self.debug("Turning Camera on")
            cubesat.cam_pin.value = True
            self.cam_on = True
            try:
                if 'images' not in os.listdir('/sd'):
                    files.mkdirp('/sd/images')
            except Exception as e:
                self.debug(f"could not initialize images directory: {e}", level=2)
        elif (not self.cam_active) and self.cam_on:
            # await self.get_confirmation(st)
            self.debug("checking camera connection...")
            await tasko.sleep(0)
            success = cubesat.camera.get_confirmation()
            if success:
                self.cam_active = True
                self.conf_attempts = 0
                alerts.clear(self.debug, 'camera_failed')
                self.debug("...connection confirmed")
            else:
                self.conf_attempts += 1
            self.check_attempts()
        elif self.cam_active and self.cam_on:
            self.debug("getting image packets")
            # get as many packets in 2 seconds as it can
            await tasko.sleep(0)
            self.get_packets(st)
        else:
            self.debug("camera asleep")
            if not iq.empty():
                self.debug(f"{iq.peek()}", level=2)
            else:
                self.debug("queue empty", level=2)

        collect()

    def check_attempts(self):
        if self.conf_attempts > MAX_CONF_ATTEMPTS:
            # turn off camera to not waste battery as something is wrong
            alerts.set(self.debug, 'camera_failed')
            cubesat.cam_pin.value = False
            self.cam_on = False
            self.cam_active = False
            self.conf_attempts = 0

    def get_packets(self, st):
        """
        camera.get_packet returns the packet and a code which gives us information about the packet
        this is why `packet, flag = cubesat.camera.get_packet`
        """
        file_err = False
        while monotonic() - 2 < st:
            packet, flag = cubesat.camera.get_packet
            if flag == flags.SUCCESS_MID_PACKET:
                # middle packet
                try:
                    with open(self.filepath, "ab") as fd:
                        fd.write(packet)
                except Exception as e:
                    file_err = True
                    print(f"could not write mid packet to {self.filepath}: {e}")
            elif flag == flags.SUCCESS_NOT_INTERESTING:
                self.debug("image not interesting")
                alerts.clear(self.debug, 'camera_failed')
                cubesat.cam_pin.value = False
                self.cam_active = False
                self.cam_on = False
                cubesat.camera.ack
                break
            elif flag == flags.SUCCESS_FIRST_PACKET:
                if cubesat.rtc:
                    t = cubesat.rtc.datetime
                else:
                    t = localtime()
                timestamp = f"{t.tm_year:04}.{t.tm_mon:02}.{t.tm_mday:02}.{t.tm_hour:02}.{t.tm_min:02}.{t.tm_sec:02}"
                self.filepath = f"/sd/images/{timestamp}.jpeg"
                self.debug(f"creating image at: {self.filepath}")
                try:
                    with open(self.filepath, "wb") as fd:
                        fd.write(packet)
                except Exception as e:
                    file_err = True
                    print(f"could not create new image file: {e}")
            elif flag == flags.SUCCESS_END_PACKET:
                self.debug("end file")
                index = packet.find(b'\xFF\xD9')
                try:
                    with open(self.filepath, "ab") as fd:
                        fd.write(packet[1:index + 2])
                    alerts.clear(self.debug, 'camera_failed')
                    cubesat.cam_pin.value = False
                    self.cam_on = False
                    self.cam_active = False
                    iq.push(self.filepath)
                    cubesat.camera.ack
                    break
                except Exception as e:
                    file_err = True
                    print(f"could not write last packet to file: {e}")
            elif flag == flags.FAIL_CONFIRM_AGAIN:
                self.debug("camera did not receive confirmation")
                self.cam_active = False
                break
            elif flag == flags.FAIL_NO_PACKET:
                self.debug("could not get packet")
                self.conf_attempts += 1
                self.check_attempts()

            if (flag == flags.SUCCESS_MID_PACKET or flag == flags.SUCCESS_FIRST_PACKET) and not file_err:
                alerts.clear(self.debug, 'camera_failed')
                self.conf_attempts = 0
                cubesat.camera.ack
