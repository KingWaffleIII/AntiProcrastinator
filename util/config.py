import json

config_path = 'config.json'
config = {
    "deadline": "2024/05/09 23:59:59",
    "blacklist": ["discord", "steam"],
    "insults": [
        "Do you want to work at McDonalds?"
    ]
}


def load_config(path: str, create: bool = True):
    """
    Load config from path.
    :param path: a string representing the path to the config file.
    :param create: whether to create the config file if it doesn't exist.
    """
    global config, config_path
    config_path = path
    try:
        with open(path) as f:
            config = json.load(f)
    except FileNotFoundError:
        if create:
            with open(path, 'w') as f:
                json.dump(config, f, indent=4)
