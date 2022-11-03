from lib.pycubed import cubesat

nvm_counters = {"c_boot": cubesat.c_boot,
                "c_state_err": cubesat.c_state_err,
                "c_vbus_rst": cubesat.c_vbus_rst,
                "c_deploy": cubesat.c_deploy,
                "c_downlink": cubesat.c_downlink,
                "c_logfail": cubesat.c_logfail}
nvm_counters_items = sorted(nvm_counters.items())
nvm_counters_values = sorted(nvm_counters.values())

def verify_bits(counterstr, counter):
    if counter is None:
        return None
    if counterstr == "c_state_err" or counterstr == "c_vbus_rst":
        return verify_four_bits(counter)
    else:
        return verify_eight_bits(counter)

def verify_four_bits(counter):
    return 0 <= counter < 16

def verify_eight_bits(counter):
    return 0 <= counter < 256

def incr_logfail_count(cubesat):
    """ increment logfail count in non-volatile memory (nvm) """
    cubesat.c_logfail += 1

def reset_logfail_count(cubesat):
    """ reset logfail count in non-volatile memory (nvm) """
    cubesat.c_logfail = 0

async def run(result_dict):
    """
    For each i2c device, print addresses of connected devices
    """
    print("Starting NVM Test...")

    nvm_counters_exist = [(counter is not None) for counter in nvm_counters_values]
    counter_access = not (False in nvm_counters_exist)
    counter_access_string = ""
    if counter_access:
        counter_access_string = "All counters are accessible."
    else:
        counter_access_string = "The following counters are None:"

    print(nvm_counters_items)
    nvm_counters_inrange = [verify_bits(counterstr, counter) for counterstr, counter in nvm_counters_items]
    counter_inrange = not (False in nvm_counters_inrange)
    counter_inrange_string = ""
    if counter_inrange:
        counter_inrange_string = "All existing counters are in range."
    else:
        counter_inrange_string = "The following counters are not in range:"

    for i in range(len(nvm_counters_values)):
        # if all counters are accessible, we'll never reach this
        # we only add to counter_access_string if something is inaccessible
        if not nvm_counters_exist[i]:
            counter_access_string += nvm_counters_items[i][0] + ";"
        # if the counter exists, verify its values
        else:
            # if all counters are in range, we'll never reach this
            # we only add to counter_inrange_string if something is out of range
            if not nvm_counters_inrange[i]:
                counter_inrange_string += nvm_counters_items[i][0] + ";"

    result_dict["NVM_CounterAccess"] = (counter_access_string, counter_access)
    result_dict["NVM_CounterValuesInRange"] = (counter_inrange_string, counter_inrange)

    print("NVM Test Complete.\n")

    return result_dict
