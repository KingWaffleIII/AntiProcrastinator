import importlib
import inspect
import json
import os
import pkgutil
from InquirerPy import inquirer

import actions
import util
from actions import Actionset
from util import Colour


def action_set_menu():
    os.system("cls")

    while True:
        action_sets = {
            "On Startup": util.config.config["on_startup"],
            "On Procrastination": util.config.config["on_procrastination"],
            "After Procrastination": util.config.config["after_procrastination"]
        }

        choice = inquirer.select(message="Select an action set or another option:", choices=[
            "On Startup",
            "On Procrastination",
            "After Procrastination",
            "Deadlines",
            "Blacklist",
            "Insults",
            "Reset to defaults",
            "Exit"
        ]).execute()

        match choice:
            case "Reset to defaults":
                confirm = inquirer.confirm(message="Are you sure you want to reset the config to defaults?").execute()
                if confirm:
                    util.config.create_config("config.json")
                    print("Config reset! Please relaunch.")
                    return

            case "Deadlines":
                for deadline in util.config.config["deadlines"]:
                    print(f"""{Colour.BOLD}{Colour.RED}{deadline}{Colour.END}""")

                action_menu("deadlines", util.config.config["deadlines"])

            case "Blacklist":
                for item in util.config.config["blacklist"]:
                    print(f"""{Colour.BOLD}{Colour.RED}{item}{Colour.END}""")

                action_menu("blacklist", util.config.config["blacklist"])

            case "Insults":
                for insult in util.config.config["insults"]:
                    print(f"""{Colour.BOLD}{Colour.RED}{insult}{Colour.END}""")

                action_menu("insults", util.config.config["insults"])

            case "Exit":
                return

            case _:
                action_set = Actionset()
                action_set.load_json(action_sets[choice])

                for action in action_set.actions:
                    text = f"""
{Colour.BOLD}{Colour.UNDERLINE}Action #{action_set.actions.index(action)+1}: {action.__class__.__name__}{Colour.END}
{Colour.RED}Condition Function:{Colour.END} {action.raw_condition_func}
"""
                    for k, v in action.to_json().items():
                        if k in ["action", "condition_func"]:
                            continue
                        text += f"{Colour.RED}{k.capitalize()}:{Colour.END} {v}\n"

                    print(text)

                action_set_name = choice.lower().replace(" ", "_")
                action_menu(action_set_name, action_set)


def get_init_params(cls):
    init_signature = inspect.signature(cls.__init__)
    params = init_signature.parameters
    return [name for name, param in params.items() if name not in ['self', 'condition_func']]


def action_menu(category: str, *args):
    while True:
        choice = inquirer.select(message="Select an option:", choices=[
            "Add",
            "Edit",
            "Remove",
            "Save",
            "Back"
        ]).execute()

        match choice:
            case "Add":
                if isinstance(args[0], Actionset):
                    action_classes = [action for action in pkgutil.iter_modules(actions.__path__) if action.name not in ["action", "actionset", "defaults"]]
                    action_classes = [action.name for action in action_classes]
                    choice = inquirer.select(message="Select an action to add:", choices=action_classes).execute()
                    module = importlib.import_module(f"actions.{choice}")
                    raw_condition_func = inquirer.text(message="Enter the condition function (leave blank for none):").execute()
                    if raw_condition_func == "":
                        raw_condition_func = None
                    params = get_init_params(getattr(module, choice.capitalize()))
                    kwargs = {"condition_func": raw_condition_func}
                    for i in params:
                        text = inquirer.text(message=f"Enter the {i}:").execute()
                        kwargs[i] = text
                    action = getattr(module, choice.capitalize())(**kwargs)
                    args[0].actions.append(action)
                else:
                    text = inquirer.text(message="Enter the new item:").execute()
                    args[0].append(text)
            case "Edit":
                if isinstance(args[0], Actionset):
                    temp = args[0].to_json()
                    choice = inquirer.select(message="Select an item to remove:", choices=[f"Action #{temp.index(action.to_json())+1}: {action.__class__.__name__}" for action in args[0].actions]).execute()
                    index = int(choice.split(" ")[1].removeprefix("#").removesuffix(":"))-1
                    action = args[0].actions[index]
                    action.raw_condition_func = inquirer.text(message="Edit the condition function:", default=action.raw_condition_func if action.raw_condition_func is not None else "None").execute()
                    for k, v in action.to_json().items():
                        if k in ["action", "condition_func"]:
                            continue
                        if isinstance(v, bool):
                            text = inquirer.select(message=f"Edit the {k}:", choices=["True", "False"]).execute()
                            action.__setattr__(k, text == "True")
                        else:
                            text = inquirer.text(message=f"Edit the {k}:", default=str(v)).execute()
                            action.__setattr__(k, text)
                    args[0].actions[index] = action
                else:
                    choice = inquirer.select(message="Select an item to edit:", choices=args[0]).execute()
                    index = args[0].index(choice)
                    text = inquirer.text(message="Edit the item:", default=args[0][index]).execute()
                    args[0][index] = text
            case "Remove":
                if isinstance(args[0], Actionset):
                    temp = args[0].to_json()
                    choice = inquirer.select(message="Select an item to remove:", choices=[f"Action #{temp.index(action.to_json())+1}: {action.__class__.__name__}" for action in args[0].actions]).execute()
                    args[0].actions.pop(int(choice.split(" ")[1].removeprefix("#").removesuffix(":"))-1)
                else:
                    choice = inquirer.select(message="Select an item to remove:", choices=args[0]).execute()
                    args[0].remove(choice)
            case "Save":
                # todo validation
                util.config.config[category] = args[0].to_json() if isinstance(args[0], Actionset) else args[0]
                util.config.save_config()
            case "Back":
                return
            case _:
                pass

        if isinstance(args[0], Actionset):
            for action in args[0].actions:
                text = f"""
{Colour.BOLD}{Colour.UNDERLINE}Action #{args[0].actions.index(action)+1}: {action.__class__.__name__}{Colour.END}
{Colour.RED}Condition Function:{Colour.END} {action.raw_condition_func}
"""
                for k, v in action.to_json().items():
                    if k in ["action", "condition_func"]:
                        continue
                    text += f"{Colour.RED}{k.capitalize()}:{Colour.END} {v}\n"

                print(text)
        else:
            for item in args[0]:
                print(f"""{Colour.BOLD}{Colour.RED}{item}{Colour.END}""")


if not util.config.config_exists("config.json"):
    util.config.create_config("config.json")
    print("Config file created!")

try:
    util.config.load_config("config.json")
    util.config.backup_config()
    action_set_menu()
except json.JSONDecodeError:
    print("Config file is invalid. Delete the file to regenerate a new one or fix the error.")
