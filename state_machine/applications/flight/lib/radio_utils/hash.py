
def bsdChecksum(bytedata):
    checksum = 0

    for b in bytedata:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += b
        checksum &= 0xffff
    return checksum
