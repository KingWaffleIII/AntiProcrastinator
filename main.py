import asyncio
import datetime
import json
import pyttsx3
import time
import win32api
from win32gui import GetWindowText, GetForegroundWindow
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)


data = json.load(open("config.json"))

EXAM = datetime.datetime.strptime(data["exam_date"], "%Y/%m/%d")

engine = pyttsx3.init()


def startup():
    engine.say(
        f"There are only {(EXAM - datetime.datetime.today()).days} days left until your exams. Time to lock in!"
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
                    f"There are only {(EXAM - datetime.datetime.today()).days} days left until your exams. Stop procrastinating retard or ISIS will be your only entryway into aerospace!"
                )
                engine.runAndWait()

                # if we paused media, play it again
                if current_session and paused:
                    await current_session.try_play_async()

                start = time.time()
                while True:
                    if window != GetWindowText(GetForegroundWindow()):
                        break
                    time.sleep(1)
                end = time.time()

                text = f"You were procrastinating for {round(end - start)} seconds on {window}! "
                print(text)
                engine.say(text + "Absolute dumbass. Do you want to work at McDonalds?")
                engine.runAndWait()

                time.sleep(60)

            time.sleep(1)
        except:
            time.sleep(60)


if __name__ == "__main__":
    startup()
    asyncio.run(main())
