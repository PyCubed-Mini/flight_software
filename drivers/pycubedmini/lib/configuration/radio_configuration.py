"""
Defines the default settings used to configure the RFM9x satellite
"""

SPREADING_FACTOR = 7
SIGNAL_BANDWIDTH = 125000
CODING_RATE = 5
CHECKSUM = True
TX_POWER = 23  # dB
FREQUENCY = 437.4  # MHz
RX_BANDWIDTH = 25.0  # KHz
PREAMBLE_LENGTH = 16  # bytes
ACK_DELAY = 0.1  # seconds
ACK_WAIT = 1  # seconds
RECEIVE_TIMEOUT = 2.0  # seconds
ACK_RETRIES = 2  # lower b/c TX queue retries as well

SATELLITE_ID = 0xAB
GROUNDSTATION_ID = 0xBA
