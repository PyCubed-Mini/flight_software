import sys
import base64
import json
import struct
from pocketqube import Pocketqube as pq


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
    if not isinstance(packet_base64, bytearray):
        packet_base64 = base64.b64decode(packet_base64)
    return pq.from_bytes(packet_base64)


def main(argv):
    if len(argv) < 1:
        print('{"error": "Invalid arguments"}')
        return 1

    try: 
        pocketqubePacket = decode(argv[0])
    except Exception as e:
        print('{"error": ' + str(e) + '}')
        return 1

    parsedPacket = {
        'header': getHeader(pocketqubePacket),
        'payload': getPayload(pocketqubePacket)
    }

    parsedPacket['telemetry'] = (parsedPacket['header']['msg_type'] == 0x02)
    
    return parsedPacket


if __name__ == '__main__':
    main(sys.argv[1:])