from state_machine import state_machine

_h = "\033["
_e = '\033[0;39;49m'

_c = {
    'red': '1',
    'green': '2',
    'orange': '3',
    'blue': '4',
    'pink': '5',
    'teal': '6',
    'white': '7',
    'gray': '9'}

_f = {
    'normal': '0',
    'bold': '1',
    'ulined': '4'}


def color_string(msg, color='gray', fmt='normal'):
    return _h + _f[fmt] + ';3' + _c[color] + 'm' + msg + _e

def debug(task_name, color, msg, level=1):
    """
    Print a debug message formatted with the task name and color

    :param msg: Debug message to print
    :type msg: str
    :param level: > 1 will print as a sub-level
    :type level: int
    """
    if level == 1:
        header = f"[{color_string(msg=task_name,color=color)}/{state_machine.state}]"
        msg = f"{header:>35} {msg}"
    else:
        msg = "\t" + f"{'   └── '}{msg}"
    print(msg)
    return msg
