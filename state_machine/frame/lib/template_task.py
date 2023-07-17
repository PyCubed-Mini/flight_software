import traceback

class Task:

    """
    Template task object.
    Stores the task name and color.
    """

    def __init__(self):
        """
        Initialize the Task
        """
        pass

    async def main_task(self, *args, **kwargs):
        """
        Contains the code for the user defined task.

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution.
        """
        pass

    async def _run(self):
        """
        Try to run the main task, then call handle_error if an error is raised.
        """
        try:
            await self.main_task()
        except Exception as e:
            await self.handle_error(e)

    async def handle_error(self, error):
        """
        Called when an error is raised in the task.
        """
        formated_exception = traceback.format_exception(error, error, error.__traceback__)
        formated_exception = '\n'.join(formated_exception)
        print(formated_exception)
