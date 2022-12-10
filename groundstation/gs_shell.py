"""
Provides a basic shell-like interface to send and receive data from the satellite
"""
from radio_utils.commands import commands
from shell_utils import bold, normal, red, green, yellow, blue, get_input_discrete, manually_configure_radio, print_radio_configuration
from gs_actions import *
import tasko

commands_by_name = {
    commands[cb]["name"]:
    {"bytes": cb, "will_respond": commands[cb]["will_respond"], "has_args": commands[cb]["has_args"]}
    for cb in commands.keys()}


async def gs_shell_main():
    print(f"\n{bold}{yellow}PyCubed-Mini Groundstation Shell{normal}\n")

    board_str = get_input_discrete(
        f"Select the board {bold}(s){normal}atellite, {bold}(f){normal}eather, {bold}(r){normal}aspberry pi",
        ["s", "f", "r"]
    )

    if board_str == "s":
        cs, reset = satellite_cs_reset()
        print(f"{bold}{green}Satellite{normal} selected")
    elif board_str == "f":
        cs, reset = feather_cs_reset()
        print(f"{bold}{green}Feather{normal} selected")
    else:  # board_str == "r"
        cs, reset = pi_cs_reset()
        print(f"{bold}{green}Raspberry Pi{normal} selected")

    radio = initialize_radio(cs, reset)

    print_radio_configuration(radio)

    if "y" == get_input_discrete(
            f"Change radio parameters? {bold}(y/N){normal}", ["", "y", "n"]):
        manually_configure_radio(radio)
        print_radio_configuration(radio)

    prompt_options = {"Receive loop": ("r", "receive"),
                      "Upload file": ("u", "upload"),
                      "Send command": ("c", "command"),
                      "Help": ("h", "print_help"),
                      "Quit": ("q", "quit")}

    def print_help():
        print(f"\n{yellow}Groundstation shell help:{normal}")
        for po in prompt_options:
            print(f"{bold}{po}{normal}: {prompt_options[po]}")

    print_help()

    while True:
        flattend_prompt_options = [v for pov in prompt_options.values() for v in pov]
        choice = get_input_discrete("Choose an action", flattend_prompt_options)
        if choice in prompt_options["Receive loop"]:
            print("Entering receive loop. CTRL-C to exit")
            while True:
                try:
                    print(await wait_for_message(radio))
                except KeyboardInterrupt:
                    break
        elif choice in prompt_options["Upload file"]:
            path = input('path= ')
            await upload_file(radio, path)
        elif choice in prompt_options["Send command"]:
            command_name = get_input_discrete("Select a command", list(commands_by_name.keys())).upper()
            command_bytes = commands_by_name[command_name]["bytes"]
            will_respond = commands_by_name[command_name]["will_respond"]
            args = input('arguments= ')
            await send_command(radio, command_bytes, args, will_respond)
        elif choice in prompt_options["Help"]:
            print_help()
        elif choice in prompt_options["Quit"]:
            break


tasko.add_task(gs_shell_main(), 1)
tasko.run()
