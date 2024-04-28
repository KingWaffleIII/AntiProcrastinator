import win32con
import win32gui
from typing import Callable

from .action import Action


class CloseWindow(Action):
    def __init__(self, condition_func: Callable[[], bool] = None):
        """
        Creates an action that closes the focused window.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

    async def execute(self):
        if not await super().execute():
            return False

        win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)

        return True
