import json

config_path = 'config.json'
config = {
    "deadline": "2024/05/09 23:59:59",
    "blacklist": ["discord", "steam"],
    "insults": [
        "Do you want to work at McDonalds?"
    ]
}


def load_config(path: str):
    """
    Load config from path.
    :param path: a string representing the path to the config file.
    """
    global config, config_path
    config_path = path
    with open(path) as f:
        config = json.load(f)
