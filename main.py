import asyncio
import datetime
import json
import pyttsx3
import win32api
from time import sleep
from win32gui import GetWindowText, GetForegroundWindow
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)


data = json.load(open("config.json"))

EXAM = datetime.datetime.strptime(data["exam_date"], "%Y/%m/%d")

VK_MEDIA_PLAY_PAUSE = 0xB3
hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)

engine = pyttsx3.init()


def startup():
    engine.say(
        f"There are {(EXAM - datetime.datetime.today()).days} days left until your exams. Time to lock in!"
    )
    engine.runAndWait()


async def main():
    while True:
        try:
            window = GetWindowText(GetForegroundWindow())
            if any(x in window.lower() for x in data["blacklist"]):
                # check if media is playing and pause it
                sessions = await MediaManager.request_async()
                current_session = sessions.get_current_session()
                paused = False
                if (
                    current_session
                    and current_session.get_playback_info().controls.is_pause_enabled
                ):
                    await current_session.try_pause_async()
                    paused = True

                engine.say(
                    f"There are {(EXAM - datetime.datetime.today()).days} days left until your exams. Stop procrastinating retard and lock in already!"
                )
                engine.runAndWait()

                # if we paused media, play it again
                if current_session and paused:
                    await current_session.try_play_async()

                sleep(60)

            sleep(1)
        except:
            sleep(60)


if __name__ == "__main__":
    startup()
    asyncio.run(main())
