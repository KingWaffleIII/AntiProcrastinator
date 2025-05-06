import datetime
import os
import random
import time
import win32gui
import win32con

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


def is_window_visible(hwnd, screen_rect):
    """
    Window visibility check that determines if a window is likely
    to be a main application window visible to the user.
    """
    # Get window style
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

    # Skip empty window titles, minimised or invisible windows, tool windows and child windows
    if (
        not win32gui.GetWindowText(hwnd)
        or not win32gui.IsWindowVisible(hwnd)
        or win32gui.IsIconic(hwnd)
        or (ex_style & win32con.WS_EX_TOOLWINDOW)
        or (style & win32con.WS_CHILD)
    ):
        return False

    try:
        window_rect = win32gui.GetWindowRect(hwnd)

        # Skip windows that are off-screen
        if (
            window_rect[2] < screen_rect[0]  # right edge < screen left
            or window_rect[0] > screen_rect[2]  # left edge > screen right
            or window_rect[3] < screen_rect[1]  # bottom edge < screen top
            or window_rect[1] > screen_rect[3]
        ):  # top edge > screen bottom
            return False

        # Skip tiny windows (likely system elements, not applications)
        width = window_rect[2] - window_rect[0]
        height = window_rect[3] - window_rect[1]
        if width < 200 or height < 100:
            return False

        # Check if it's the foreground window
        foreground_hwnd = win32gui.GetForegroundWindow()
        if hwnd == foreground_hwnd:
            return True

        # Calculate window size and visible area threshold
        window_area = width * height
        min_visible_area = (
            window_area * 0.2
        )  # Window is visible if at least 20% is showing

        # Find windows that could be obscuring this one
        obscuring_windows = []

        def enum_obscuring_windows(other_hwnd, _data):
            if (
                other_hwnd != hwnd
                and win32gui.IsWindowVisible(other_hwnd)
                and not win32gui.IsIconic(other_hwnd)
            ):

                # Get Z-order - only consider windows above this one
                # Use GetWindow with GW_HWNDPREV to walk the Z-order
                test_hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDPREV)
                is_above = False
                while test_hwnd:
                    if test_hwnd == other_hwnd:
                        is_above = True
                        break
                    test_hwnd = win32gui.GetWindow(test_hwnd, win32con.GW_HWNDPREV)

                if is_above:
                    try:
                        other_rect = win32gui.GetWindowRect(other_hwnd)
                        # Check for overlap
                        if (
                            other_rect[0] < window_rect[2]
                            and other_rect[2] > window_rect[0]
                            and other_rect[1] < window_rect[3]
                            and other_rect[3] > window_rect[1]
                        ):
                            if not any(
                                x in win32gui.GetWindowText(other_hwnd).lower()
                                for x in ["sharex"]
                            ):
                                obscuring_windows.append((other_hwnd, other_rect))
                    except Exception:
                        pass
            return True

        win32gui.EnumWindows(enum_obscuring_windows, None)

        # Calculate visible area (simplified)
        obscured_area = 0
        for _, obscuring_rect in obscuring_windows:
            # Calculate intersection area
            overlap_left = max(window_rect[0], obscuring_rect[0])
            overlap_top = max(window_rect[1], obscuring_rect[1])
            overlap_right = min(window_rect[2], obscuring_rect[2])
            overlap_bottom = min(window_rect[3], obscuring_rect[3])

            if overlap_right > overlap_left and overlap_bottom > overlap_top:
                overlap_area = (overlap_right - overlap_left) * (
                    overlap_bottom - overlap_top
                )
                obscured_area += overlap_area

        visible_area = window_area - obscured_area
        return visible_area >= min_visible_area

    except Exception as e:
        print(f"Error checking window visibility: {e}")
        return False


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
