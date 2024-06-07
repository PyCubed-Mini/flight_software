# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Pocketqube(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Pocketqube.Header(self._io, self, self._root)
        _on = self.header.msg_type
        if _on == 0:
            self.payload = Pocketqube.Default(self._io, self, self._root)
        elif _on == 249:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 251:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 252:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 253:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 248:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 2:
            self.payload = Pocketqube.Beacon(self._io, self, self._root)
        elif _on == 255:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 250:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 247:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)
        elif _on == 254:
            self.payload = Pocketqube.Buffered(self._io, self, self._root)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.msg_type = self._io.read_u1()


    class Default(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.message = (self._io.read_bytes_full()).decode(u"ASCII")


    class Beacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.time_min = self._io.read_u1()
            self.time_sec = self._io.read_u1()
            self.state_index = self._io.read_u1()
            self.datetime_valid_flag = self._io.read_u1()
            self.contact_flag = self._io.read_u1()
            self.burn_flag = self._io.read_u2be()
            self.software_error_count = self._io.read_f4be()
            self.boot_count = self._io.read_f4be()
            self.battery_voltage = self._io.read_f4be()
            self.cpu_temperature_c = self._io.read_f4be()
            self.imu_temperature_c = self._io.read_f4be()
            self.gyro_0 = self._io.read_f4be()
            self.gyro_1 = self._io.read_f4be()
            self.gyro_2 = self._io.read_f4be()
            self.mag_0 = self._io.read_f4be()
            self.mag_1 = self._io.read_f4be()
            self.mag_2 = self._io.read_f4be()
            self.rssi_db = self._io.read_f4be()
            self.fei_hz = self._io.read_f4be()
            self.lux_xp = self._io.read_f4be()
            self.lux_yp = self._io.read_f4be()
            self.lux_zp = self._io.read_f4be()
            self.lux_xn = self._io.read_f4be()
            self.lux_yn = self._io.read_f4be()
            self.lux_zn = self._io.read_f4be()


    class Buffered(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes_full()



