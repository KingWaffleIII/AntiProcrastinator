import actions

# Available actions:
# actions.Sleep
# actions.Say
# actions.Exit
# actions.Playsound
# actions.Closewindow
# actions.Notify

# Wildcards:
# {deadline} -> get_deadline()
# {insult} -> get_insult()
# {timer_diff} -> get_timer_diff_in_text()
# {window} -> window

# Condition functions should be lambdas.
# Avoid using Python, rather use the available functions in util.functions.
# If you want to use something not implemented, you can add it to util/functions.py.

OnStartupActionSet = actions.Actionset(
    [
        actions.Say(
            text="Good luck bro, the deadline has passed.",
            pause_media=True,
            condition_func="lambda: util.functions.has_deadline_passed()",
        ),
        actions.Exit(
            condition_func="lambda: util.functions.has_deadline_passed()",
        ),
        actions.Say(
            text="{deadline}Time to lock in!",
            pause_media=True,
            condition_func=None,
        ),
    ]
)

OnProcrastinationActionSet = actions.Actionset(
    [
        actions.Say(
            text="{deadline}{insult}",
            pause_media=True,
            condition_func="lambda: not util.functions.check_timer_elapsed_time(60)",
        ),
        actions.Sleep(
            sleep_time=60,
            condition_func="lambda: not util.functions.check_timer_elapsed_time(60)",
        ),
        actions.Say(
            text="Nah you're finished, you've been procrastinating for {timer_diff}! {insult}",
            pause_media=True,
            condition_func=None,
        ),
        actions.Playsound(
            file_path=r"{runtime_dir}\annoying.mp3",
        ),
    ]
)

AfterProcrastinationActionSet = actions.Actionset(
    [
        actions.Notify(
            # text="[{timestamp}] You were procrastinating for {timer_diff} on {window}!"
            text="You were procrastinating for {timer_diff} on {window}!"
        ),
        actions.Say(
            text="You retard, you were procrastinating for {timer_diff}! {insult}",
            pause_media=True,
            condition_func=None,
        ),
    ]
)

BreakActionSet = actions.Actionset(
    [
        actions.Say(
            text="Well done, you can relax for a bit.",
            pause_media=True,
            condition_func=None,
        ),
        actions.Sleep(600),
        actions.Say(
            text="Break's over! Get back to work, those A's aren't gonna earn themselves.",
            pause_media=True,
            condition_func=None,
        ),
    ]
)
