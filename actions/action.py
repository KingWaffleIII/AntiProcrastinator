from typing import Callable

import util


class Action:
    def __init__(self, condition_func: str = None):
        """
        Creates an action.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
        """
        self.raw_condition_func = condition_func
        self.condition_func: Callable[[], bool] = eval(condition_func) if condition_func is not None else None
        pass

    def from_json(self, json: list):
        condition_func = json['condition_func']
        if condition_func is not None:
            json['condition_func'] = util.functions.build_condition_function(
                condition_func['function'],
                condition_func['inverse'],
                condition_func['args']
            )
        args = {k: v for k, v in json.items() if k != 'action'}
        return self.__class__(**args)

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

        return {"action": "Action", "condition_func": condition_func}

    async def execute(self) -> bool:
        """
        Checks the condition function and executes the action.
        :return: whether the action was executed.
        """
        try:
            if self.condition_func is not None and not self.condition_func():
                return False
            return True
        except Exception as e:
            print(e)
            return False
