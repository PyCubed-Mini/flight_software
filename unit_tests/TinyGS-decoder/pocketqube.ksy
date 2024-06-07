meta:
  id: pocketqube
  file-extension: pocketqube
  endian: be
seq:
  - id: header
    type: header
  - id: payload
    type:
      switch-on: header.msg_type
      cases:
        0x00: default
        0x02: beacon
        0xff: buffered
        0xfe: buffered
        0xfd: buffered
        0xfc: buffered
        0xfb: buffered
        0xfa: buffered
        0xf9: buffered
        0xf8: buffered
        0xf7: buffered
        
types:
  header:
    seq:
    - id: msg_type
      type: u1
      
  default:
    seq:
      - id: message
        type: str
        encoding: ASCII
        size-eos: true
  
  beacon:
    seq:
      - id: time_min
        type: u1
      - id: time_sec
        type: u1
      - id: state_index
        type: u1
      - id: datetime_valid_flag
        type: u1
      - id: contact_flag
        type: u1
      - id: burn_flag
        type: u2
      - id: software_error_count
        type: f4
      - id: boot_count
        type: f4
      - id: battery_voltage
        type: f4
      - id: cpu_temperature_c
        type: f4
      - id: imu_temperature_c
        type: f4
      - id: gyro_0
        type: f4
      - id: gyro_1
        type: f4
      - id: gyro_2
        type: f4
      - id: mag_0
        type: f4
      - id: mag_1
        type: f4
      - id: mag_2
        type: f4
      - id: rssi_db
        type: f4
      - id: fei_hz
        type: f4
      - id: lux_xp
        type: f4
      - id: lux_yp
        type: f4
      - id: lux_zp
        type: f4
      - id: lux_xn
        type: f4
      - id: lux_yn
        type: f4
      - id: lux_zn
        type: f4
      
  buffered:
    seq:
      - id: data
        size-eos: true
