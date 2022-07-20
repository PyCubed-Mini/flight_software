"""
Python system check script for PyCubed satellite board
PyCubed Mini mainboard-v02 for Pocketqube Mission
SD Card Logging Test
* Author(s): Yashika Batra
"""

from os import exists, remove

def sd_test():
    """
    Run a basic test; create a file and test existence, write to and read from a file,
    delete file and test existence. Return result_dict values accordingly
    """

    # create file
    test_fp = "/sd/test.txt"
    test_file = open(test_fp)

    # check that the file exists:
    if not exists(test_fp):
        return ("Created a file but system says it does not exist.", False)

    # write to file
    test_string = "Hello World! This is a test file.\n"
    test_file.write(test_string)
    test_file.close()

    # read from file
    test_file_read = open(test_fp)
    test_string_read = test_file_read.read()
    if test_string_read != test_string:
        return ("File not written to or read from correctly.", False)

    # delete file
    remove(test_file)

    # check that the file no longer exists:
    if exists(test_fp):
        return ("File not successfully deleted.", False)

    return ("SD Card passed all tests: Created, wrote to, " +
            "read from, and deleted a file successfully.", True)


def run(hardware_dict, result_dict):
    """
    Check that the correct hardware is initialized and run tests
    """

    # if no SD Card detected, update result dictionary and return
    if not hardware_dict['SDcard']:
        result_dict['SDcard_Logging'] = ('Cannot test logging; no SD Card detected', False)
        return result_dict

    # if SD Card detected, run other tests
    result_val_string, result_val_bool = sd_test()
    result_dict['SDcard_Logging'] = (result_val_string, result_val_bool)
    return result_dict
