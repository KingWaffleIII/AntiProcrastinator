import pyttsx3

from .action import Action


class Say(Action):
    def __init__(self, text: str, pause_media=True, condition_func: str = None, **kwargs):
        """
        Creates an action that converts text to speech.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
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
        return {"action": "Say", "condition_func": condition_func, "text": self.text, "pause_media": self.pause_media, "kwargs": self.engine_kwargs}

    async def execute(self) -> bool:
        if not await super().execute():
            return False

        import util

        paused = False
        if self.pause_media:
            paused = await util.functions.pause_media()

        text = util.functions.replace_wildcards(self.text)

        self.engine.say(text)
        self.engine.runAndWait()

        if paused:
            await util.functions.play_media()

        return True
