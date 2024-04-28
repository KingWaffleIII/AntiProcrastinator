from typing import Callable

import util
from .action import Action


class Print(Action):
    def __init__(self, text: str, condition_func: Callable[[], bool] = None, *args, **kwargs):
        """
        Creates an action that prints to the console.
        :param text: the text to print.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

        self.text = text
        self.args = args
        self.kwargs = kwargs

    async def execute(self):
        if not await super().execute():
            return False

        text = util.functions.replace_wildcards(self.text)
        print(text, *self.args, **self.kwargs)
