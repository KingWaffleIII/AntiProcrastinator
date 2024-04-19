import asyncio
import datetime
import json
import multiprocessing
import playsound
import pyttsx3
import random
import sys
import time
import win32gui
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)

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


def get_deadline():
    deadline = datetime.datetime.strptime(json.load(open("config.json"))["deadline"], "%Y/%m/%d %H:%M:%S")
    diff = deadline - datetime.datetime.today()
    if diff.days > 1:
        return f"There are only {diff.days} days left until your deadline. "
    if diff.days == 1:
        diff = int((diff - datetime.timedelta(days=1)).total_seconds() / 60 / 60)
        return f"My brother in Christ, there are only {diff + 24} hours left until your deadline. "
    time = get_time(int(diff.total_seconds()))
    if any(x in time for x in ["hour", "minute", "second"]):
        return f"Bro you're cooked, there is only {time} left until your deadline. "
    return f"Bro you're cooked, there are only {time} left until your deadline. "


def get_insult():
    data = json.load(open("config.json"))
    return data["insults"][random.randint(0, len(data["insults"]) - 1)]


async def startup():
    deadline = datetime.datetime.strptime(json.load(open("config.json"))["deadline"], "%Y/%m/%d %H:%M:%S")
    diff = int((deadline - datetime.datetime.today()).total_seconds())
    if diff < 0:
        await say("Good luck bro, the deadline has passed.")
        sys.exit(0)

    await say(
        get_deadline() + "Time to lock in!"
    )


async def watcher():
    while True:
        try:
            data = json.load(open("config.json"))
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if any(x in window.lower() for x in data["blacklist"]):
                await say(
                    get_deadline() + get_insult()
                )

                annoying_proc = None
                super_annoying_proc = None
                start = time.time()

                while True:
                    new_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    if window != new_window and new_window != '':
                        break
                    diff = round(time.time() - start)

                    # every minute
                    if diff > 0 and diff % 60 == 0:
                        if annoying_proc is not None:
                            annoying_proc.kill()
                            annoying_proc = None

                        await say(
                            f"Nah you're finished, you've been procrastinating for {get_time(diff)} on {window}! " + get_insult()
                        )
                        time.sleep(1)

                        # 1 minute
                        if diff >= 60 and annoying_proc is None:
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
                    time.sleep(1)

                if annoying_proc is not None:
                    annoying_proc.kill()

                diff = round(time.time() - start)
                if diff > 0:
                    notice = (
                        f"You retard, you were procrastinating for {get_time(diff)} on {window}! "
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
