import datetime
import random
import time
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)

from . import config


def get_time(t: int):
    """
    Get time in human-readable format.  e.g. 3600 -> 1 hour, 60 -> 1 minute, 1 -> 1 second
    :param t: total time in seconds.
    :return: string of human-readable time.
    """
    if t % 60 == 0:
        if t > 3600:
            return f"{t // 3600} hour{'s' if t // 3600 > 1 else ''}"
        if t > 60:
            return f"{t // 60} minute{'s' if t // 60 > 1 else ''}"
    if t > 3600:
        return f"{t // 3600} hour{'s' if t // 3600 > 1 else ''}, {t % 3600 // 60} minute{'s' if t % 3600 // 60 > 1 else ''} and {t % 3600 % 60} second{'s' if t % 3600 % 60 > 1 else ''}"
    if t > 60:
        return f"{t // 60} minute{'s' if t // 60 > 1 else ''} and {t % 60} second{'s' if t % 60 > 1 else ''}"
    return f"{t} second{'s' if t > 1 or t == 0 else ''}"


def get_raw_deadline():
    """
    Get deadline from config as datetime object.
    :return: the deadline as datetime object.
    """
    config.load_config(config.config_path)
    return datetime.datetime.strptime(config.config["deadline"], "%Y/%m/%d %H:%M:%S")


def get_deadline_now_diff():
    """
    Get difference between deadline and current time in seconds.
    :return: difference between deadline and current time in seconds.
    """
    deadline = get_raw_deadline()
    return int((deadline - datetime.datetime.today()).total_seconds())


def get_deadline():
    """
    Get deadline in human-readable format.
    :return: the deadline in human-readable format.
    """
    deadline = get_raw_deadline()
    diff = deadline - datetime.datetime.today()
    if diff.days > 1:
        return f"There are only {diff.days} days left until your deadline. "
    if diff.days == 1:
        diff = int((diff - datetime.timedelta(days=1)).total_seconds() / 60 / 60)
        return f"My brother in Christ, there are only {diff + 24} hours left until your deadline. "
    t = get_time(int(diff.total_seconds()))
    if any(x in t for x in ["hour", "minute", "second"]):
        return f"Bro you're cooked, there is only {t} left until your deadline. "
    return f"Bro you're cooked, there are only {t} left until your deadline. "


def get_insult():
    """
    Get random insult from config.
    :return: random insult.
    """
    config.load_config(config.config_path)
    return config.config["insults"][random.randint(0, len(config.config["insults"]) - 1)]


async def pause_media():
    """
    Pauses any currently playing media.
    """
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if (
            current_session
            and current_session.get_playback_info().controls.is_pause_enabled
    ):
        await current_session.try_pause_async()


async def play_media():
    """
    Plays any paused media.
    """
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    await current_session.try_play_async()

timer = time.time()


def start_timer():
    """
    Start the timer.
    """
    global timer
    timer = time.time()


def get_timer_diff() -> float:
    """
    Get difference between timer and current time in seconds.
    :return: difference between timer and current time in seconds.
    """
    return time.time() - timer


def check_timer_elapsed_time(t: int) -> bool:
    """
    Check if time elapsed is greater than t.
    :param t: time in seconds.
    :return: whether time elapsed is greater than t.
    """
    return time.time() - timer > t


def get_timer_diff_in_text() -> str:
    """
    Get timer difference in human-readable format.
    :return: timer difference in human-readable format.
    """
    return get_time(round(get_timer_diff()))


def replace_wildcards(text: str) -> str:
    """
    Replace custom wildcards in text.
    {deadline} -> get_deadline()
    {insult} -> get_insult()
    {timer_diff} -> get_timer_diff_in_text()
    :param text: text to replace wildcards in.
    :return: text with wildcards replaced.
    """
    return (
        text
        .replace("{deadline}", get_deadline())
        .replace("{insult}", get_insult())
        .replace("{timer_diff}", get_timer_diff_in_text())
    )

