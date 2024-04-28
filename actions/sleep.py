import asyncio
from typing import Callable

from .action import Action


class Sleep(Action):
    def __init__(self, sleep_time: int, condition_func: Callable[[], bool] = None):
        """
        Creates an action that sleeps (blocking), pausing the ActionSet.
        :param sleep_time: the time to sleep in seconds.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

        self.sleep_time = sleep_time

    async def execute(self):
        if not await super().execute():
            return False

        await asyncio.sleep(self.sleep_time)

        return True
