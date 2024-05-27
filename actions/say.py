import pyttsx3

from .action import Action


class Say(Action):
    def __init__(self, text: str, pause_media=True, condition_func: str = None):
        """
        Creates an action that converts text to speech.
        :param condition_func: the condition to check before executing the action, as a string cast lambda function.
        :param text: text to say.
        :param pause_media: whether to pause media when speaking.
        """

        super().__init__(condition_func)

        self.text = text
        self.pause_media = pause_media

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)

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
        return {"action": "Say", "condition_func": condition_func, "text": self.text, "pause_media": self.pause_media}

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
