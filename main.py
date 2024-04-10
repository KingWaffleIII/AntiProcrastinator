import asyncio
import datetime
import json
import multiprocessing
import playsound
import pyttsx3
import random
import time
from win32gui import GetWindowText, GetForegroundWindow
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)

exam = datetime.datetime.strptime(json.load(open("config.json"))["exam_date"], "%Y/%m/%d")

engine = pyttsx3.init()
engine.setProperty("rate", 175)


async def say(text):
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

    engine.say(text)
    engine.runAndWait()

    # if we paused media, play it again
    if paused:
        await current_session.try_play_async()


def get_time(time: int):
    if time % 60 == 0:
        if time > 3600:
            return f"{time // 3600} hour{'s' if time // 3600 > 1 else ''}"
        if time > 60:
            return f"{time // 60} minute{'s' if time // 60 > 1 else ''}"
    if time > 3600:
        return f"{time // 3600} hour{'s' if time // 3600 > 1 else ''}, {time % 3600 // 60} minute{'s' if time % 3600 // 60 > 1 else ''} and {time % 3600 % 60} second{'s' if time % 3600 % 60 > 1 else ''}"
    if time > 60:
        return f"{time // 60} minute{'s' if time // 60 > 1 else ''} and {time % 60} second{'s' if time % 60 > 1 else ''}"
    return f"{time} second{'s' if time > 1 else ''}"


def get_insult():
    data = json.load(open("config.json"))
    return data["insults"][random.randint(0, len(data["insults"]) - 1)]


async def startup():
    await say(
        f"There are only {(exam - datetime.datetime.today()).days} days left until your exams. Time to lock in!"
    )


async def watcher():
    while True:
        try:
            data = json.load(open("config.json"))
            window = GetWindowText(GetForegroundWindow())
            if any(x in window.lower() for x in data["blacklist"]):
                await say(
                    f"There are only {(exam - datetime.datetime.today()).days} days left until your exams. " + get_insult()
                )

                annoying_proc = None
                super_annoying_proc = None
                start = time.time()

                while True:
                    new_window = GetWindowText(GetForegroundWindow())
                    if window != new_window and new_window != '':
                        break
                    diff = round(time.time() - start)

                    # every minute
                    if diff > 0 and diff % 60 == 0:
                        if annoying_proc is not None:
                            annoying_proc.kill()
                        if super_annoying_proc is not None:
                            super_annoying_proc.kill()

                        await say(
                            f"You've been procrastinating for {get_time(diff)} on {window}! " + get_insult()
                        )
                        time.sleep(1)

                        # 1 minute
                        if diff == 60 and annoying_proc is None:
                            await say(
                                "Domain Expansion: Kurukuru Kururin!"
                            )

                            # check if media is playing and pause it
                            sessions = await MediaManager.request_async()
                            current_session = sessions.get_current_session()
                            if (
                                    current_session
                                    and current_session.get_playback_info().controls.is_pause_enabled
                            ):
                                await current_session.try_pause_async()

                            annoying_proc = multiprocessing.Process(target=playsound.playsound, args=("annoying.mp3",))
                            annoying_proc.start()

                        # 2 minutes
                        if diff == 120 and super_annoying_proc is None:
                            await say(
                                "Domain Expansion: Femur Breaker!"
                            )

                            # check if media is playing and pause it
                            sessions = await MediaManager.request_async()
                            current_session = sessions.get_current_session()
                            if (
                                    current_session
                                    and current_session.get_playback_info().controls.is_pause_enabled
                            ):
                                await current_session.try_pause_async()

                            super_annoying_proc = multiprocessing.Process(target=playsound.playsound, args=("super_annoying.mp3",))
                            super_annoying_proc.start()
                    time.sleep(1)

                if annoying_proc is not None:
                    annoying_proc.kill()
                if super_annoying_proc is not None:
                    super_annoying_proc.kill()

                diff = round(time.time() - start)
                if diff > 0:
                    notice = (
                        f"You were procrastinating for {get_time(diff)} on {window}! "
                    )
                    print(notice)
                    await say(
                        notice + get_insult()
                    )

                time.sleep(60)

            time.sleep(1)
        except:
            time.sleep(60)


if __name__ == "__main__":
    asyncio.run(startup())
    asyncio.run(watcher())
