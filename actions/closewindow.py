import win32con
import win32gui

from .action import Action


class Closewindow(Action):
    def __init__(self, condition_func: str = None):
        """
        Creates an action that closes the focused window.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
        """
        super().__init__(condition_func)

    def to_json(self):
        """
        Converts the action to JSON.
        :return: JSON representation of the action.
        """
        import util

        if self.condition_func is not None:
            condition_func_str = util.functions.deconstruct_condition_function(self.raw_condition_func)
            condition_func = {
                "function": condition_func_str[0],
                "inverse": condition_func_str[1],
                "args": condition_func_str[2]
            }
        else:
            condition_func = None

        return {"action": "Closewindow", "condition_func": condition_func}

    async def execute(self):
        if not await super().execute():
            return False

        win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)

        return True
