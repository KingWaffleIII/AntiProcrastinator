import asyncio
import multiprocessing
import os
import sys
import threading
import time

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


notif_recv_conn, notif_send_conn = multiprocessing.Pipe()


def notify_worker():
    while True:
        try:
            if notif_recv_conn.poll(0.1):
                notif = notif_recv_conn.recv()
                print(f"Got notification: {notif}")

                # Try using pystray notification
                if hasattr(icon, "_thread") and getattr(icon, "visible", False):
                    try:
                        print("Trying to notify with pystray...")
                        icon.notify(notif)
                        print("Notification sent with pystray")
                        continue  # Skip to next notification if successful
                    except Exception as e:
                        print(f"Pystray notification failed: {e}")
                else:
                    print("Icon not ready for notification")
            else:
                time.sleep(0.5)

        except Exception as e:
            print(f"Notification worker error: {e}")
            time.sleep(1)


icon = pystray.Icon(
    "AntiProcrastinator",
    Image.open(functions.eval_file_path(r"{runtime_dir}\icon.png")),
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
