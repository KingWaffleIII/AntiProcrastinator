import asyncio

from .action import Action


class Sleep(Action):
    def __init__(self, sleep_time: int, condition_func: str = None):
        """
        Creates an action that sleeps (blocking), pausing the ActionSet.
        :param sleep_time: the time to sleep in seconds.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

        self.sleep_time = sleep_time

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
        return {"action": "Sleep", "condition_func": condition_func, "sleep_time": self.sleep_time}

    async def execute(self):
        if not await super().execute():
            return False

        await asyncio.sleep(self.sleep_time)

        return True
