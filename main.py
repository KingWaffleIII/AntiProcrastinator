import asyncio
import multiprocessing
import multiprocessing.popen_spawn_win32 as forking
import os
import time
import sys
import win32gui

import util
import actions

util.config.load_config("config.json", create=True)


# Freeze support for multiprocessing when using PyInstaller.
class _Popen(forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            # We have to set original _MEIPASS2 value from sys._MEIPASS
            # to get --onefile mode working.
            os.putenv('_MEIPASS2', sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                # available. In those cases we cannot delete the variable
                # but only set it to the empty string. The bootloader
                # can handle this case.
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')


class Process(multiprocessing.Process):
    _Popen = _Popen


OnStartupActionSet = actions.ActionSet()
OnProcrastinationActionSet = actions.ActionSet()
AfterProcrastinationActionSet = actions.ActionSet()

# Available actions:
# actions.Sleep
# actions.Say
# actions.Exit
# actions.PlaySound
# actions.CloseWindow
# actions.Print

# Wildcards:
# {deadline} -> get_deadline()
# {insult} -> get_insult()
# {timer_diff} -> get_timer_diff_in_text()
# {window} -> window

OnStartupActionSet.add_actions(
    [
        actions.Say(
            text="Good luck bro, the deadline has passed.",
            pause_media=True,
            condition_func=lambda: util.vars.is_deadline_now_diff_negative,
            rate=175,
        ),
        actions.Exit(
            condition_func=lambda: util.vars.is_deadline_now_diff_negative,
        ),
        actions.Say(
            text="{deadline}Time to lock in!",
            pause_media=True,
            condition_func=None,
            rate=175,
        ),
    ]
)

OnProcrastinationActionSet.add_actions(
    [
        actions.Say(
            text="{deadline}{insult}", pause_media=True, condition_func=None, rate=175
        ),
        actions.Sleep(
            sleep_time=60,
        ),
        actions.Say(
            text="Nah you're finished, you've been procrastinating for {timer_diff}! {insult}",
            pause_media=True,
            condition_func=None,
            rate=175,
        ),
        actions.PlaySound(
            file_path=os.path.dirname(__file__) + r"\\annoying.mp3",
        ),
    ]
)

AfterProcrastinationActionSet.add_actions(
    [
        actions.Print(text="You were procrastinating for {timer_diff} on {window}!"),
        actions.Say(
            text="You retard, you were procrastinating for {timer_diff}! {insult}",
            pause_media=True,
            condition_func=None,
            rate=175,
        ),
    ]
)


async def startup():
    await OnStartupActionSet.execute()


def procrastination():
    while True:
        asyncio.run(OnProcrastinationActionSet.execute())


async def watch():
    proc = None
    while True:
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if window != "" and any(
            x in window.lower() for x in util.config.config["blacklist"]
        ):
            if proc is None or not proc.is_alive():
                util.functions.start_timer()
                util.functions.set_window(window)
                proc = Process(target=procrastination)
                proc.start()
        else:
            if proc is not None and proc.is_alive():
                proc.kill()
                proc = None

                await AfterProcrastinationActionSet.execute()

                time.sleep(60)

        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    asyncio.run(startup())
    asyncio.run(watch())
