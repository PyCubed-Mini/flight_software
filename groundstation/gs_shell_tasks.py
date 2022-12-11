from gs_commands import *


async def send_command_task(radio, command_bytes, args, will_respond, debug=False):
    success, response = send_command(radio, command_bytes, args, will_respond, debug=debug)
    if success:
        print("Command successful")
        print(f"Response: {response}")
    else:
        print("Command failed")

async def read_loop(radio):

    while True:
        header, message = await wait_for_message(radio)
        print_message(header, message)
