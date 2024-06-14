import sys
import base64
import struct
import json

def getPayload(packet):
    telemetry_names = (
        'tm_min',
        'tm_sec',
        'state_index',
        'flags',
        'software_error',
        'boot_count',
        'vbatt',
        'cpu_temp',
        'imu_temp',
        'gyro0',
        'gyro1',
        'gyro2',
        'mag0',
        'mag1',
        'mag2',
        'rssi',
        'fei',
        'lux_xp',
        'lux_yp',
        'lux_zp',
        'lux_xn',
        'lux_yn',
        'lux_zn'
    )
    return {k:v for (k, v) in zip(telemetry_names, packet)}
    

def decode(packet_base64):
    # Specific telemetry format
    format = 2 * 'H' + 3 * 'B' + 'H' + 'f' * 11 + 6 * 'f'
    packet_struct = base64.b64decode(packet_base64)
    return struct.unpack(format, packet_struct[1:])

def main(argv):
    if len(argv) < 1:
        print('{"error": "Invalid arguments"}')
        return 1

    try:
        prometheus_packet = decode(argv[0])
    except Exception as e:
        print('{"error": ' + str(e) + '}')
        return 1
        
    parsed_packet = {
        'payload': getPayload(prometheus_packet)
    }

    parsed_packet['telemetry'] = True

    print(json.dumps(parsed_packet))
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])