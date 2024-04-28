from typing import Callable


class Action:
    def __init__(self, condition_func: Callable[[], bool] = None):
        """
        Creates an action.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        self.condition_func = condition_func
        pass

    async def execute(self) -> bool:
        """
        Checks the condition function and executes the action.
        :return: whether the action was executed.
        """
        if self.condition_func is not None and not self.condition_func():
            return False
        return True
