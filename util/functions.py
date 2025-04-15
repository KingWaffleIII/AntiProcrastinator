import asyncio
import datetime
import os
import random
import sys
import time

import pystray
from PIL import Image
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)

from . import config


def is_valid_datetime(date: str) -> bool:
    """
    Check if a string is a valid datetime.
    :param date: a string representing a datetime.
    :return: whether the string is a valid datetime.
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


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

    # deprecated
    # if isinstance(config.config["deadlines"], str):
    #     return datetime.datetime.strptime(config.config["deadlines"], "%Y/%m/%d %H:%M:%S")

    # list of deadlines
    for i in config.config["deadlines"]:
        # check if datetime has passed
        if (
            datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
            > datetime.datetime.today()
        ):
            return datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")


def get_deadline_now_diff():
    """
    Get difference between deadline and current time in seconds.
    :return: difference between deadline and current time in seconds.
    """
    deadline = get_raw_deadline()
    return int((deadline - datetime.datetime.today()).total_seconds())


def has_deadline_passed():
    """
    Check if the deadline has passed.
    :return: whether the deadline has passed.
    """
    return get_deadline_now_diff() < 0


def get_deadline():
    """
    Get deadline in human-readable format.
    :return: the deadline in human-readable format.
    """
    try:
        deadline = get_raw_deadline()
        diff = deadline - datetime.datetime.today()
        if diff.days > 1:
            return f"There are only {diff.days} days left until your deadline. "
        if diff.days == 1:
            diff = int((diff - datetime.timedelta(days=1)).total_seconds() / 60 / 60)
            return f"My brother in Christ, there are only {diff + 24} hours left until your deadline. "
        t = get_time(int(diff.total_seconds()))
        # if any(x in t for x in ["hour", "minute", "second"]):
        #     return f"Bro you're cooked, there is only {t} left until your deadline. "
        return f"Bro you're cooked, there are only {t} left until your deadline. "
    except TypeError:  # no deadline
        return "You have not configured a deadline but that doesn't mean you can slack off. "


def get_insult():
    """
    Get random insult from config.
    :return: random insult.
    """
    config.load_config(config.config_path)
    return config.config["insults"][
        random.randint(0, len(config.config["insults"]) - 1)
    ]


async def pause_media() -> bool:
    """
    Pauses any currently playing media.
    :return: whether media was paused.
    """
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if (
        current_session
        and current_session.get_playback_info().controls.is_pause_enabled
    ):
        await current_session.try_pause_async()
        return True

    return False


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
    Start the global timer.
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


window = ""


def set_window(w: str):
    """
    Sets the global window.
    :param w: the window to set.
    """
    global window
    window = w


def replace_wildcards(text: str) -> str:
    """
    Replace custom wildcards in text.
    {deadline} -> get_deadline()
    {insult} -> get_insult()
    {timer_diff} -> get_timer_diff_in_text()
    {window} -> window
    {timestamp} -> current timestamp (HH:MM:SS)
    :param text: text to replace wildcards in.
    :return: text with wildcards replaced.
    """
    return (
        text.replace("{deadline}", get_deadline())
        .replace("{insult}", get_insult())
        .replace("{timer_diff}", get_timer_diff_in_text())
        .replace("{window}", window)
        .replace("{timestamp}", datetime.datetime.now().strftime("%H:%M:%S"))
    )


def eval_file_path(text: str) -> str:
    """
    Evaluates {runtime_dir} in text.
    :return: the evaluated text.
    """
    return text.replace(
        "{runtime_dir}", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )


def build_condition_function(function: str, inverse: bool, args: list) -> str:
    """
    Builds a condition function from a string for use in actions.
    :param function: the function that will be evaluated.
    :param inverse: whether to add "not".
    :param args: args for the function.
    :return: a lambda function as a string.
    """
    if len(args) != 0:
        args_str = "".join([f"{arg}," for arg in args])[:-1]
    else:
        args_str = ""
    if inverse:
        return f"lambda: not {function}({args_str})"
    return f"lambda: {function}({args_str})"


def deconstruct_condition_function(condition_func: str) -> tuple[str, bool, list]:
    """
    Deconstructs a condition function into its parts.
    :param condition_func: the condition function to deconstruct.
    :return: a tuple containing the function, whether it is inverted and the args.
    """
    condition_func = condition_func.replace("lambda: ", "")
    inverse = condition_func.startswith("not ")
    condition_func = condition_func.replace("not ", "")
    function = condition_func.split("(")[0]
    args = condition_func.split("(")[1].replace(")", "").split(",")
    if args == [""]:
        args = []
    return function, inverse, args


def run_configurator():
    if not hasattr(sys, "frozen"):
        os.system('start cmd /k "python configurator.py"')
    else:
        # run configutator.exe
        os.system("configurator.exe")


def take_break():
    from actions import Actionset

    BreakActionSet = Actionset()
    BreakActionSet.load_json(config.config["break"])
    asyncio.get_event_loop().run_until_complete(BreakActionSet.execute())


icon = pystray.Icon(
    "AntiProcrastinator",
    Image.open(eval_file_path(r"{runtime_dir}\icon2.png")),
    title="AntiProcrastinator",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Open Configurator",
            run_configurator,
        ),
        pystray.MenuItem(
            "Break",
            take_break,
        ),
        pystray.MenuItem(
            "Exit",
            lambda icon: (icon.stop(), os._exit(0)),
        ),
    ),
)
