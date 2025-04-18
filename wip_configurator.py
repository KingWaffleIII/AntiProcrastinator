import json
import threading
import webbrowser
import copy

from flask import Flask, jsonify, redirect, render_template, request
from waitress import serve

import util
import actions

# instance of flask application
app = Flask(__name__)

PORT = 5000

if not util.config.config_exists("config.json"):
    util.config.create_config("config.json")


with open("config.json") as f:
    config = json.load(f)

action_sets = {
    "on_startup": config["on_startup"],
    "on_procrastination": config["on_procrastination"],
    "after_procrastination": config["after_procrastination"],
    "break": config["break"],
}


def reload_action_sets():
    global action_sets
    action_sets = {
        "on_startup": config["on_startup"],
        "on_procrastination": config["on_procrastination"],
        "after_procrastination": config["after_procrastination"],
        "break": config["break"],
    }


def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    reload_action_sets()


@app.route("/")
def action():
    return render_template("actions.html")


@app.route("/actions/<action_set>")
def actionsets(action_set):
    actionset = actions.Actionset()
    action_set_json = copy.deepcopy(action_sets[action_set])
    actionset.load_json(action_set_json)
    actions_list = []
    for action in actionset.actions:
        action_json = {
            "name": action.__class__.__name__,
            "condition_func": action.raw_condition_func,
        }
        for k, v in action.to_json().items():
            if k in ["action", "condition_func"]:
                continue
            action_json[k] = v
        actions_list.append(action_json)
    return render_template(
        "actionset.html",
        name=action_set,
        actions=actions_list,
    )


@app.route("/actions/<action_set>/remove/<int:item>")
def actionsets_remove(action_set, item):
    actionset = actions.Actionset()
    action_set_json = copy.deepcopy(action_sets[action_set])
    actionset.load_json(action_set_json)
    item: actions.Action = actionset.actions[item]
    actionset.remove_action(item)
    config[action_set] = actionset.to_json()
    save_config()
    return redirect(f"/actions/{action_set}")


@app.route("/deadlines")
def deadlines():
    return render_template("deadlines.html", deadlines=config["deadlines"])


@app.route("/deadlines/add")
def deadlines_add():
    if "item" in request.args:
        config["deadlines"].append(request.args["item"])
    save_config()
    return redirect("/deadlines")


@app.route("/deadlines/remove/<int:item>")
def deadlines_remove(item):
    config["deadlines"].pop(item)
    save_config()
    return redirect("/deadlines")


@app.route("/blacklist")
def blacklist():
    return render_template("blacklist.html", blacklist=config["blacklist"])


@app.route("/blacklist/add")
def blacklist_add():
    if "item" in request.args:
        config["blacklist"].append(request.args["item"])
    save_config()
    return redirect("/blacklist")


@app.route("/blacklist/remove/<int:item>")
def blacklist_remove(item):
    config["blacklist"].pop(item)
    save_config()
    return redirect("/blacklist")


@app.route("/whitelist")
def whitelist():
    return render_template("whitelist.html", whitelist=config["whitelist"])


@app.route("/whitelist/add")
def whitelist_add():
    if "item" in request.args:
        config["whitelist"].append(request.args["item"])
    save_config()
    return redirect("/whitelist")


@app.route("/whitelist/remove/<int:item>")
def whitelist_remove(item):
    config["whitelist"].pop(item)
    save_config()
    return redirect("/whitelist")


@app.route("/insults")
def insults():
    return render_template("insults.html", insults=config["insults"])


@app.route("/insults/add")
def insults_add():
    if "item" in request.args:
        config["insults"].append(request.args["item"])
    save_config()
    return redirect("/insults")


@app.route("/insults/remove/<int:item>")
def insults_remove(item):
    config["insults"].pop(item)
    save_config()
    return redirect("/insults")


if __name__ == "__main__":
    # threading.Thread(
    #     target=webbrowser.open, args=("http://localhost:" + str(PORT),), daemon=True
    # ).start()
    app.run(host="localhost", port=PORT, debug=True)
    # serve(app, port=PORT)
