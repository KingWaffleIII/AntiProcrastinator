# AntiProcrastinator

A Python script that yells at you for doing things you shouldn't be. Yes, I was procrastinating when I made this.

Features:

- Immediately yells at you on launch
- Monitors the focused window and yells at you if you're procrastinating
    - Matches blacklisted strings in the window name
- Pauses any media you're playing to yell at you
- Regularly reminds you how close your deadline is
- Customisable insults
- Realtime config changes (no need to restart the script)
- Completely customisable actions (e.g. play a sound, print to console, etc.)
  - Extending the project and adding your own actions is very simple by simply extending `action.Action`.
  - You can make actions from emailing someone to shutting down your computer.


## Usage:

- Set the `deadline` in `config.json`
- Add any phrases you want to `blacklist` (e.g. discord, steam) for the focused window in `config.json`
- Edit the `insults` in `config.json` to your liking

Example:

```json
{
    "deadline": "2024/05/09 23:59:59",
    "blacklist": ["discord", "steam"],
    "insults": [
    "Do you want to work at McDonalds?"
    ]
}

```

- (recommended) Add to Task Scheduler or equivalent (put the executable in `shell:common startup` in Windows Explorer) to run on startup

This runs the script on startup and in the background.
Enable this if you use Task Scheduler else TTS will not work:

![Run only when user is logged on (checked)](image.png)

You can run the Python script or the executable in `dist/`, **make sure to have `config.json` in the same directory**.
