import sys
import base64
import json
import struct
from pocketqube import Pocketqube as pq


# Mutating function that takes in a dictionary
# and returns a list representation of the bytes
def formatPacket(d):
    del d['_io']
    del d['_parent']
    del d['_root']
    for key in d:
        if isinstance(d[key], bytes):
            d[key] = list(d[key])


def getHeader(packet):
    pkt = packet.header.__dict__.copy()
    formatPacket(pkt)
    return pkt


def getPayload(packet):
    pkt = packet.payload.__dict__.copy()
    formatPacket(pkt)
    return pkt


def decode(packet_base64):
    fmt = 2 * 'H' + 3 * 'B' + 'H' + 'f' * 11 + 6 * 'f'
    if not isinstance(packet_base64, bytearray):
        #base64_bytes = packet_base64.encode('ascii')

        packet_base64 = base64.b64decode(packet_base64)
    # unpacked_array = bytearray([])
    # unpacked = struct.unpack(fmt, packet_base64[1:])
    # for val in unpacked:
    #     unpacked_array += bytearray(val.to_bytes((val.bit_length() + 7) // 8, 'big'))
    return pq.from_bytes(packet_base64)


def main(argv):
    if len(argv) < 1:
        print('{"error": "Invalid arguments"}')
        return 1

    try: 
        pocketqubePacket = decode(argv[0])
        print(pocketqubePacket.payload.boot_count)
    except Exception as e:
        print('{"error": ' + str(e) + '}')
        return 1
    
    # We must check if the packet that was recieved is a telemetry packet
    # if it is not a telemetry packet then it won't get passed along however
    # if it is a telemetry packet it does get passed along

    parsedPacket = {
        'header': getHeader(pocketqubePacket),
        'payload': getPayload(pocketqubePacket)
    }

    parsedPacket['telemetry'] = (parsedPacket['header']['msg_type'] == 0x02)
    
    #print(json.dumps(parsedPacket))
    return parsedPacket


if __name__ == '__main__':
    main(sys.argv[1:])