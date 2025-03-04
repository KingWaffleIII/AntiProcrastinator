import datetime
import json

config_path = 'config.json'
config = {}


def load_config(path: str):
    """
    Load config from path.
    :param path: a string representing the path to the config file.
    """
    global config, config_path
    config_path = path
    try:
        with open(path) as f:
            config = json.load(f)
    except FileNotFoundError:
        pass


def backup_config():
    """
    Backs up the config to another config file.
    """
    with open(config_path + '.bak', 'w') as f:
        json.dump(config, f, indent=4)


def save_config():
    """
    Save the config to the config file.
    """
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)


def config_exists(path: str) -> bool:
    """
    Check if a config file exists at the given path.
    :param path: a string representing the path to the config file.
    :return: whether a config file exists at the given path.
    """
    try:
        with open(path) as f:
            return True
    except FileNotFoundError:
        return False


def create_config(path: str):
    """
    Create a config file at the given path.
    :param path: a string representing the path to the config file.
    """
    with open(path, 'w+') as f:
        from actions import defaults

        config = {
            "deadlines": [(datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")],
            "blacklist": ["discord", "steam"],
            "whitelist": [],
            "insults": [
                "Do you want to work at McDonalds?"
            ],
            "on_startup": defaults.OnStartupActionSet.to_json(),
            "on_procrastination": defaults.OnProcrastinationActionSet.to_json(),
            "after_procrastination": defaults.AfterProcrastinationActionSet.to_json(),
        }
        json.dump(config, f, indent=4)
