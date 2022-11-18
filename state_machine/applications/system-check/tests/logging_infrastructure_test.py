"""
Python System Check Module for PyCubed Mini satellite board
Logging Infrastructure Test: Time Based, Buffered and Unbuffered Logging
"""

from logging import clear_all_storage, get_buffer, log
from os import listdir
from lib.pycubed import cubesat
import time

sd_card_directory = "/sd"

async def run(result_dict):
    """
    If the SD card has been properly initialized, log 1800 characters
    100 characters at a time, with a max file size of 1000 characters.
    Make sure that 2 files have been created as a result of these logs.
    """

    if not cubesat.sdcard:
        print("Cannot test Logging Infrastructure; no SD Card detected")
        result_dict["LoggingInfrastructure_Test"] = (
            "Cannot test Logging Infrastructure; no SD Card detected", None)

    print("Starting logging infrastructure test...")

    print(f"Initial, /sd/: {listdir(sd_card_directory)}")
    clear_all_storage()
    print(f"After clearing storage, /sd/: {listdir(sd_card_directory)}")

    # unbuffered write
    print("Testing buffered vs. unbuffered writes...")
    # for each folder in the folders array
    sd_buffer = get_buffer()
    buffer_working = True
    folder1_written = True
    folder2_written = True

    folders = ["folder1", "folder2"]
    # length = 40 characters
    msg1 = f"Testing buffered write! Folder: {folders[0]}\n"
    msg2 = f"Testing buffered write! Folder: {folders[1]}\n"
    msgs = [msg1, msg2]

    for i in range(len(folders)):
        filenum = 0
        buffer_written = 0
        max_buffer_size = 200
        msg = msgs[i] * 10

        # write 2 files worth of messages (sleep 5 seconds between writes)
        while filenum < 2:
            # write buffered logs
            log(msg, folder=folders[i], buffer=True, max_buffer_size=max_buffer_size)

            # if buffer is empty, increment count
            if sd_buffer[folders[i]] == "":
                buffer_written += 1

            # increment number of files written
            filenum += 1

            # sleep (waiting for the next file's creation)
            time.sleep(5)

        # check if the buffer was emptied out the correct number of times
        buffer_working = buffer_working and buffer_written >= len(msg) // max_buffer_size - 1


    # check if folder1 has all the correct logfiles
    if folders[0] in listdir(sd_card_directory):
        for folderfile in listdir(f"{sd_card_directory}/{folders[0]}/logs"):
            folderfile_reader = open(
                f"{sd_card_directory}/{folders[0]}/logs/{folderfile}", "r")
            folderfile_string = folderfile_reader.read()
            if (msgs[0] not in folderfile_string or
                    len(listdir(f"{sd_card_directory}/{folders[0]}")) < 2):
                folder1_written = False
    else:
        print("Folder1 not created.")
        folder1_written = False

    # check if folder2 has all the correct logfiles
    if folders[1] in listdir(sd_card_directory):
        for folderfile in listdir(f"{sd_card_directory}/{folders[1]}/logs"):
            folderfile_reader = open(
                f"{sd_card_directory}/{folders[1]}/logs/{folderfile}", "r")
            folderfile_string = folderfile_reader.read()
            if (msgs[1] not in folderfile_string or
                    len(listdir(f"{sd_card_directory}/{folders[1]}")) < 2):
                folder2_written = False
    else:
        print("Folder2 not created.")
        folder2_written = False

    if buffer_working:
        print("Buffer is correctly updated.")
    else:
        print("Buffer is not correctly updated.")

    if folder1_written:
        print("Folder 1 has the correct message written to its files.")
    else:
        print("Folder 1's files do not contain the correct message.")

    if folder2_written:
        print("Folder 2 has the correct message written to its files.")
    else:
        print("Folder 2's files do not contain the correct message.")

    print("Testing unbuffered vs. buffered writes is complete.")
    print(f"/sd/ directory: {listdir(sd_card_directory)}")
    for folder in listdir(sd_card_directory):
        if folder in folders:
            folder_logs_contents = listdir(f'{sd_card_directory}/{folder}/logs/')
            print(f"logs in /sd/{folder} directory: {folder_logs_contents}")

    if folder1_written and folder2_written:
        result_string = ("Both folders have been written to correctly." +
                         " Please perform any necessary manual checks.")
    else:
        result_string = ("Some folder was not written to correctly." + 
                         " Please check above messages to troubleshoot.")
    print(result_string)
    result_dict["LoggingInfrastructure_Test"] = (
        result_string, folder1_written and folder2_written)
    print("Logging Infrastructure Test complete.\n")

    print(f"Ending, /sd/: {listdir(sd_card_directory)}")
    clear_all_storage()
    print(f"After Clearing Storage, /sd/: {listdir(sd_card_directory)}")
