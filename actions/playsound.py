import playsound

from .action import Action


class PlaySound(Action):
    def __init__(self, file_path: str, condition_func: str = None):
        """
        Creates an action that plays a sound file.
        Note: if using Pyinstaller, add the sound file to AntiProcrastinator.spec.
        :param file_path: the path to the sound file.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
        """
        super().__init__(condition_func)

        self.file_path = file_path

    def to_json(self):
        """
        Converts the action to JSON.
        :return: JSON representation of the action.
        """
        import util

        if self.raw_condition_func is not None:
            condition_func_str = util.functions.deconstruct_condition_function(self.raw_condition_func)
            condition_func = {
                "function": condition_func_str[0],
                "inverse": condition_func_str[1],
                "args": condition_func_str[2]
            }
        else:
            condition_func = None
        return {"action": "PlaySound", "condition_func": condition_func, "file_path": self.file_path}

    async def execute(self):
        if not await super().execute():
            return False

        import util

        await util.functions.pause_media()

        playsound.playsound(util.functions.eval_file_path(self.file_path))
