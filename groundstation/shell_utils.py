"""
A collection of functions for getting and validating inputs
"""

# print formatters
bold = '\033[1m'
normal = '\033[0m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'

def get_input_discrete(prompt_str, choice_values):
    print(prompt_str)
    choice = None

    choice_values_str = "("
    for i, _ in enumerate(choice_values):
        choice_values_str += f"{choice_values[i]}"
        if i < len(choice_values) - 1:
            choice_values_str += ", "
    choice_values_str += ")"

    choice_values = [cv.lower() for cv in choice_values]

    while choice not in choice_values:
        choice = input(f"{choice_values_str} ~> ").lower()
    return choice


def set_param_from_input_discrete(param, prompt_str, choice_values, allow_default=False, type=int):

    # add "enter" as a choice
    choice_values = [""] + choice_values if allow_default else choice_values
    prompt_str = prompt_str + \
        " (enter to skip):" if allow_default else prompt_str

    choice = get_input_discrete(prompt_str, choice_values)

    if choice == "":
        return param
    else:
        return type(choice)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_input_range(prompt_str, choice_range):
    print(prompt_str)
    choice = None

    choice_range_str = f"({choice_range[0]} - {choice_range[1]})"

    while True:
        choice = input(f"{choice_range_str} ~> ").lower()
        if choice == "":
            break

        if not is_number(choice):
            continue

        if float(choice) >= choice_range[0] and float(choice) <= choice_range[1]:
            break
    return choice


def set_param_from_input_range(param, prompt_str, choice_range, allow_default=False):

    # add "enter" as a choice
    prompt_str = prompt_str + \
        " (enter to skip):" if allow_default else prompt_str

    choice = get_input_range(prompt_str, choice_range)

    if choice == "":
        return param
    else:
        return float(choice)

def manually_configure_radio(radio):
    radio.frequency_mhz = set_param_from_input_range(radio.frequency_mhz, f"Frequency (currently {radio.frequency_mhz} MHz)",
                                                     [240.0, 960.0], allow_default=True)
    radio.tx_power = set_param_from_input_discrete(radio.tx_power, f"Power (currently {radio.tx_power} dB)",
                                                   [f"{i}" for i in range(5, 24)], allow_default=True)
    radio.bitrate = set_param_from_input_range(radio.bitrate, f"Bitrate (currently {radio.bitrate} bps)",
                                               [500, 300000], allow_default=True)
    radio.frequency_deviation = set_param_from_input_range(radio.frequency_deviation, f"Frequency deviation (currently {radio.frequency_deviation})",
                                                           [600, 200000], allow_default=True)
    radio.rx_bandwidth = set_param_from_input_discrete(radio.rx_bandwidth, f"Receiver filter bandwidth (single-sided, currently {radio.rx_bandwidth})",
                                                       [f"{radio._bw_bins_kHz[i]}" for i in range(len(radio._bw_bins_kHz))], allow_default=True, type=float)
    radio.lna_gain = set_param_from_input_discrete(radio.lna_gain, f"LNA Gain - [max = 1, min = 6] (currently {radio.lna_gain})",
                                                   [f"{i}" for i in range(1, 7)], allow_default=True)
    radio.preamble_length = set_param_from_input_range(radio.preamble_length, f"Preamble length (currently {radio.preamble_length})",
                                                       [3, 2**16], allow_default=True)
    radio.ack_delay = set_param_from_input_range(radio.ack_delay, f"Acknowledge delay (currently {radio.ack_delay} s)",
                                                 [0.0, 10.0], allow_default=True)
    radio.ack_wait = set_param_from_input_range(radio.ack_wait, f"Acknowledge RX Timeout (currently {radio.ack_wait} s)",
                                                [0.0, 100.0], allow_default=True)
    radio.afc_enable = set_param_from_input_discrete(radio.afc_enable, f"Enable automatic frequency calibration (AFC) (currently {radio.afc_enable})",
                                                     ["0", "1"], allow_default=True)

def print_radio_configuration(radio):
    print(f"{yellow}{bold}Radio Configuration:{normal}")
    print(f"\tNode addr = {radio.node}\tDest addr = {radio.destination}")
    print(f"\tFrequency = {radio.frequency_mhz} MHz")
    print(f"\tPower = {radio.tx_power} dBm")
    print(f"\tBitrate = {radio.bitrate} Hz")
    print(f"\tFrequency Deviation = {radio.frequency_deviation}")
    print(f"\tRX filter bandwidth = {radio.rx_bandwidth}")
    print(f"\tLNA Gain [max = 1, min = 6] = {radio.lna_gain}")
    print(f"\tPreamble Length = {radio.preamble_length}")
    print(f"\tAcknowledge delay = {radio.ack_delay} s")
    print(f"\tAcknowledge wait = {radio.ack_wait} s")
    print(f"\tAFC enabled = {radio.afc_enable}")
