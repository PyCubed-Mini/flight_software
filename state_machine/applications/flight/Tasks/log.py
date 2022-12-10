from lib.template_task import Task
from pycubed import cubesat
import logs
import traceback
import os

log_fd = None
log_fd_str = None

class Task(Task):

    def debug(self, msg, level=1, log=False):
        """
        Print a debug message formatted with the task name and color.
        Also log the message to a log file if log is set to True.

        :param msg: Debug message to print
        :type msg: str
        :param level: > 1 will print as a sub-level
        :type level: int
        :param log: Whether to log the message to a file
        :type log: bool
        """
        msg = super().debug(msg, level)
        if cubesat.sdcard and log:
            try:
                self.log(msg)
            except Exception as e:
                # shouldn't call self.debug to prevent never ending loop
                print(f'Error logging to file: {e}')

    def log(self, msg):
        """
        Log a message to a log file.
        """
        t = cubesat.rtc.datetime
        hour_stamp = f'{t.tm_year}.{t.tm_mon}.{t.tm_mday}.{t.tm_hour}'
        new_log_fd_str = f'/sd/logs/debug/{hour_stamp}.txt'
        global log_fd
        global log_fd_str
        if new_log_fd_str != log_fd_str:
            if log_fd is not None:
                log_fd.close()
            try:
                log_fd = open(new_log_fd_str, 'a')
            except Exception:
                logs.try_mkdir('/sd/logs/')
                logs.try_mkdir('/sd/logs/debug/')
                log_fd = open(new_log_fd_str, 'a')
            log_fd_str = new_log_fd_str

        log_fd.write(f'[{logs.human_time_stamp()}]\n')
        log_fd.write(msg)
        log_fd.write('\n')

    async def handle_error(self, error):
        """
        Called when an error is raised in the task.
        Logs it to the debug logs.
        """
        formated_exception = traceback.format_exception(error, error, error.__traceback__)
        self.debug(f'[Error] {formated_exception}', log=True)
