import asyncio
import multiprocessing
import os
import time
import win32gui

import util
import actions

util.config.load_config("config.json")

OnStartupActionSet = actions.ActionSet()
OnProcrastinationActionSet = actions.ActionSet(repeat=True)
AfterProcrastinationActionSet = actions.ActionSet()

# Available actions:
# actions.Sleep
# actions.Say
# actions.Exit
# actions.PlaySound
# actions.CloseWindow

# Wildcards:
# {deadline} -> get_deadline()
# {insult} -> get_insult()
# {timer_diff} -> get_timer_diff_in_text()

OnStartupActionSet.add_actions([
    actions.Say(
        text="Good luck bro, the deadline has passed.",
        pause_media=True,
        condition_func=lambda: util.vars.is_deadline_now_diff_negative,
        rate=175
    ),
    actions.Exit(
        condition_func=lambda: util.vars.is_deadline_now_diff_negative,
    ),
    actions.Say(
        text="{deadline}Time to lock in!",
        pause_media=True,
        condition_func=None,
        rate=175
    ),
])

OnProcrastinationActionSet.add_actions([
    actions.Say(
        text="{deadline}{insult}",
        pause_media=True,
        condition_func=None,
        rate=175
    ),
    actions.Sleep(
        sleep_time=60,
    ),
    actions.Say(
        text="Nah you're finished, you've been procrastinating for {timer_diff}! {insult}",
        pause_media=True,
        condition_func=None,
        rate=175
    ),
    actions.PlaySound(
        file_path=os.path.dirname(__file__) + r"\\annoying.mp3",
    )
])

AfterProcrastinationActionSet.add_actions([
    actions.Say(
        text="You retard, you were procrastinating for {timer_diff}! {insult}",
        pause_media=True,
        condition_func=None,
        rate=175
    )
])


async def startup():
    await OnStartupActionSet.execute()


def procrastination():
    asyncio.run(OnProcrastinationActionSet.execute())


async def watch():
    proc = None
    while True:
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if any(x in window.lower() for x in util.config.config["blacklist"]):
            if proc is None or not proc.is_alive():
                util.functions.start_timer()
                proc = multiprocessing.Process(target=procrastination)
                proc.start()
        else:
            if proc is not None and proc.is_alive():
                proc.kill()
                proc = None

                await AfterProcrastinationActionSet.execute()

                time.sleep(60)

        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(startup())
    asyncio.run(watch())
