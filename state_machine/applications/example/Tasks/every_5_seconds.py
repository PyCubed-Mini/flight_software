from lib.template_task import Task


class task(Task):

    async def main_task(self):
        print('This task runs every 5 seconds')
