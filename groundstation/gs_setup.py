"""
Provides individual groundstation actions such as upload a file,
wait for packet, or send a command.
"""
import board
import busio
import digitalio
from lib import pycubed_rfm9x_fsk
from lib.configuration import radio_configuration as rf_config
from shell_utils import bold, normal

def initialize_radio(cs, reset):
    """
    Initialize the radio - uses lib/configuration/radio_configuration to configure with defaults
    """

    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    radio = pycubed_rfm9x_fsk.RFM9x(
        spi,
        cs,
        reset,
        rf_config.FREQUENCY,
        checksum=rf_config.CHECKSUM)

    # configure to match satellite
    radio.tx_power = rf_config.TX_POWER
    radio.bitrate = rf_config.BITRATE
    radio.frequency_deviation = rf_config.FREQUENCY_DEVIATION
    radio.rx_bandwidth = rf_config.RX_BANDWIDTH
    radio.preamble_length = rf_config.PREAMBLE_LENGTH
    radio.ack_delay = rf_config.ACK_DELAY
    radio.ack_wait = rf_config.ACK_WAIT
    radio.node = rf_config.GROUNDSTATION_ID
    radio.destination = rf_config.SATELLITE_ID

    return radio

def satellite_cs_reset():
    # pocketqube
    cs = digitalio.DigitalInOut(board.RF_CS)
    reset = digitalio.DigitalInOut(board.RF_RST)
    cs.switch_to_output(value=True)
    reset.switch_to_output(value=True)

    radio_DIO0 = digitalio.DigitalInOut(board.RF_IO0)
    radio_DIO0.switch_to_input()
    radio_DIO1 = digitalio.DigitalInOut(board.RF_IO1)
    radio_DIO1.switch_to_input()

    return cs, reset

def feather_cs_reset():
    # feather
    cs = digitalio.DigitalInOut(board.D5)
    reset = digitalio.DigitalInOut(board.D6)
    cs.switch_to_output(value=True)
    reset.switch_to_output(value=True)

    return cs, reset

def pi_cs_reset():
    cs = digitalio.DigitalInOut(board.CE1)
    reset = digitalio.DigitalInOut(board.D25)

    return cs, reset
