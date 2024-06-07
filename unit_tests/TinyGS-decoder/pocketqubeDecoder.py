import sys
import base64
import json
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
    if isinstance(packet_base64, bytearray):
        message_bytes = base64.b64decode(packet_base64)
    else:
        base64_bytes = packet_base64.encode('latin-1')
        message_bytes = base64.b64decode(base64_bytes)
    return pq.from_bytes(message_bytes)


def main(argv):
    if len(argv) < 1:
        print('{"error": "Invalid arguments"}')
        return 1

    try: 
        pocketqubePacket = decode(argv[0])
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

    parsedPacket['telemetry'] = (parsedPacket['header']['message'] == 0x02)
    
    print(json.dumps(parsedPacket))
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])