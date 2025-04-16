import asyncio
import multiprocessing
import os
import sys
import threading

import pystray
from PIL import Image

from . import config, functions


class Colour:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def run_configurator():
    if not hasattr(sys, "frozen"):
        os.system('start cmd /k "python configurator.py"')
    else:
        # run configutator.exe
        os.system("configurator.exe")


break_event = multiprocessing.Event()


def take_break():
    break_event.set()
    icon.update_menu()

    from actions import Actionset

    BreakActionSet = Actionset()
    BreakActionSet.load_json(config.config["break"])

    def run_break():
        asyncio.run(BreakActionSet.execute())
        break_event.clear()
        icon.update_menu()

    threading.Thread(target=run_break, daemon=True).start()


icon = pystray.Icon(
    "AntiProcrastinator",
    Image.open(functions.eval_file_path(r"{runtime_dir}\icon2.png")),
    title="AntiProcrastinator",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Open Configurator",
            run_configurator,
        ),
        pystray.MenuItem(
            "Break",
            take_break,
            enabled=lambda icon: not break_event.is_set(),
        ),
        pystray.MenuItem(
            "Exit",
            lambda icon: icon.stop(),
        ),
    ),
)
