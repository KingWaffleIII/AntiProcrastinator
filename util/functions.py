import datetime
import os
import random
import time

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
    Get time in human-readable format. e.g. 86400 -> 1 day, 3600 -> 1 hour, 60 -> 1 minute
    :param t: total time in seconds.
    :return: string of human-readable time.
    """
    days = t // (24 * 3600)
    t = t % (24 * 3600)
    hours = t // 3600
    t = t % 3600
    minutes = t // 60
    seconds = t % 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 or (days == 0 and hours == 0 and minutes == 0):
        parts.append(f"{seconds} second{'s' if seconds > 1 or seconds == 0 else ''}")

    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    else:
        return ", ".join(parts[:-1]) + f" and {parts[-1]}"


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


def get_pure_deadline():
    """
    Get only the deadline in human-readable format.
    :return: the deadline in human-readable format.
    """
    try:
        return get_time(get_deadline_now_diff())
    except Exception:  # no deadline
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


def replace_wildcards(text: str) -> str:
    """
    Replace custom wildcards in text.
    {deadline} -> get_deadline()
    {pure_deadline} -> get_pure_deadline()
    {insult} -> get_insult()
    {timer_diff} -> get_timer_diff_in_text()
    {timestamp} -> current timestamp (HH:MM:SS)
    :param text: text to replace wildcards in.
    :return: text with wildcards replaced.
    """
    return (
        text.replace("{deadline}", get_deadline())
        .replace("{pure_deadline}", get_pure_deadline())
        .replace("{insult}", get_insult())
        .replace("{timer_diff}", get_timer_diff_in_text())
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


_process_notif_conn = None


def set_notification_pipe(conn):
    """
    Set the notification pipe connection for this process.
    """
    global _process_notif_conn
    _process_notif_conn = conn


def show_notif(notif: str) -> None:
    """
    Shows a notification via the tray icon.
    :param notif: the notification to show.
    """
    # Use the process-specific connection if available
    if _process_notif_conn is not None:
        _process_notif_conn.send(notif)
