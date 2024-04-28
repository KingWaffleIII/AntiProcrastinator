from typing import Callable

from .action import Action


class Exit(Action):
    def __init__(self, condition_func: Callable[[], bool] = None):
        """
        Creates an action that exits the program.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

    async def execute(self):
        if not await super().execute():
            return False

        exit(0)
