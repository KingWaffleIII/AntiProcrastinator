from util import icon

from .action import Action


class Notify(Action):
    def __init__(self, text: str, condition_func: str = None):
        """
        Creates an action that sends a desktop notification.
        :param text: the text to send.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
        """
        super().__init__(condition_func)

        self.text = text

    def to_json(self):
        """
        Converts the action to JSON.
        :return: JSON representation of the action.
        """
        import util

        if self.condition_func is not None:
            condition_func_str = util.functions.deconstruct_condition_function(
                self.raw_condition_func
            )
            condition_func = {
                "function": condition_func_str[0],
                "inverse": condition_func_str[1],
                "args": condition_func_str[2],
            }
        else:
            condition_func = None
        return {"action": "Notify", "condition_func": condition_func, "text": self.text}

    async def execute(self):
        if not await super().execute():
            return False

        import util

        text = util.functions.replace_wildcards(self.text)
        icon.notify(text)
