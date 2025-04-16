import asyncio
import json
import multiprocessing
import multiprocessing.popen_spawn_win32 as forking
import os
import sys
import time

import win32gui

import actions
import util

if not util.config.config_exists("config.json"):
    # print("Config file not found. Please run the configurator first.")
    # sys.exit(-1)
    util.config.create_config("config.json")
    print("Config file created!")

try:
    util.config.load_config("config.json")
except json.JSONDecodeError:
    print("Config file is invalid. Please run the configurator.")
    sys.exit(-1)


# Freeze support for multiprocessing when using PyInstaller.
class _Popen(forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, "frozen"):
            # We have to set original _MEIPASS2 value from sys._MEIPASS
            # to get --onefile mode working.
            os.putenv("_MEIPASS2", sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, "frozen"):
                # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                # available. In those cases we cannot delete the variable
                # but only set it to the empty string. The bootloader
                # can handle this case.
                if hasattr(os, "unsetenv"):
                    os.unsetenv("_MEIPASS2")
                else:
                    os.putenv("_MEIPASS2", "")


OnStartupActionSet = actions.Actionset()
OnProcrastinationActionSet = actions.Actionset()
AfterProcrastinationActionSet = actions.Actionset()

OnStartupActionSet.load_json(util.config.config["on_startup"])
OnProcrastinationActionSet.load_json(util.config.config["on_procrastination"])
AfterProcrastinationActionSet.load_json(util.config.config["after_procrastination"])


class Process(multiprocessing.Process):
    _Popen = _Popen


async def startup():
    await OnStartupActionSet.execute()


def procrastination():
    while True:
        asyncio.run(OnProcrastinationActionSet.execute())


async def watch(break_event: multiprocessing.Event):
    proc = None
    while True:
        if break_event.is_set():
            raise asyncio.CancelledError

        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if (
            window
            and any(x in window.lower() for x in util.config.config["blacklist"])
            and not any(x in window.lower() for x in util.config.config["whitelist"])
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


def run_watchdog(break_event: multiprocessing.Event):
    while True:
        if not break_event.is_set():
            try:
                asyncio.run(watch(break_event))
            except asyncio.CancelledError:
                continue
        else:
            time.sleep(1)


if __name__ == "__main__":
    multiprocessing.freeze_support()

    asyncio.run(startup())

    watchdog = Process(target=run_watchdog, args=(util.break_event,), name="watchdog")
    watchdog.start()

    try:
        util.icon.run()
    finally:
        if watchdog.is_alive():
            watchdog.kill()
