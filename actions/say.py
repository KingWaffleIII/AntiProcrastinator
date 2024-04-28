import pyttsx3
from typing import Callable

import util
from .action import Action


class Say(Action):
    def __init__(self, text: str, pause_media=True, condition_func: Callable[[], bool] = None, **kwargs):
        """
        Creates an action that converts text to speech.
        :param condition_func: the condition to check before executing the action, as a function.
        :param text: text to say.
        :param pause_media: whether to pause media when speaking.
        :param kwargs: kwargs for pyttsx3 engine.
        """

        super().__init__(condition_func)

        self.text = text
        self.pause_media = pause_media
        self.engine_kwargs = kwargs

        self.engine = pyttsx3.init()
        for k, v in self.engine_kwargs.items():
            self.engine.setProperty(k, v)

    async def execute(self) -> bool:
        if not await super().execute():
            return False

        paused = False
        if not self.pause_media:
            await util.functions.pause_media()
            paused = True

        text = util.functions.replace_wildcards(self.text)

        self.engine.say(text)
        self.engine.runAndWait()

        if paused:
            await util.functions.play_media()

        return True
