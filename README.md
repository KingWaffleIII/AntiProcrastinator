# AntiProcrastinator

Your computer will yell at you for procrastinating. Yes, I was procrastinating when I made this.

Features:

- Immediately yells at you on launch
- Monitors the focused window and yells at you if you're procrastinating
    - Matches blacklisted strings in the window name
- Pauses any media you're playing to yell at you
- Regularly reminds you how close your exam(s) are
- Customisable insults
- Realtime config changes (no need to restart the script)


## Usage:

- Set the `exam_date` in `config.json`
- Add any phrases you want to `blacklist` (e.g. discord, steam) for the focused window in `config.json`
- Edit the `insults` in `config.json` to your liking

Example:

```json
{
    "exam_date": "2024/05/09",
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
