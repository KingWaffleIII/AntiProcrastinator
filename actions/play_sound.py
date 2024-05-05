import playsound
from typing import Callable

import util
from .action import Action


class PlaySound(Action):
    def __init__(self, file_path: str, condition_func: Callable[[], bool] = None):
        """
        Creates an action that plays a sound file.
        Note: if using Pyinstaller, add the sound file to AntiProcrastinator.spec.
        :param file_path: the path to the sound file.
        :param condition_func: the condition to check before executing the action, as a function.
        """
        super().__init__(condition_func)

        self.file_path = file_path

    async def execute(self):
        if not await super().execute():
            return False

        await util.functions.pause_media()

        playsound.playsound(self.file_path)
