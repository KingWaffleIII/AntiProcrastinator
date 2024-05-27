# AntiProcrastinator

A Python script that yells at you for doing things you shouldn't be. Yes, I was procrastinating when I made this.

Features:

- Immediately yells at you on launch
- Monitors the focused window and yells at you if you're procrastinating
    - Matches blacklisted strings in the window name
- Pauses any media you're playing to yell at you
- Regularly reminds you how close your deadline is
- Customisable insults
- Realtime config changes (no need to restart the program)
- Completely customisable actions (e.g. play a sound, print to console, etc.)
  - Extending the project and adding your own actions is very simple by simply extending `action.Action`.
  - You can make actions from emailing someone to shutting down your computer.

## Usage:

- [Download the latest release](https://github.com/KingWaffleIII/AntiProcrastinator/releases) and run once.
- Run `configurator.exe` to edit the config.
- Run `AntiProcrastinator.exe`!

  - **Available actions:**
    - `Sleep`
    - `Say`
    - `Exit`
    - `Playsound`
    - `Closewindow`
    - `Print`

  - **Wildcards:**
    - `{deadline}` -> `get_deadline()`
    - `{insult}` -> `get_insult()`
    - `{timer_diff}` -> `get_timer_diff_in_text()`
    - `{window}` -> `window`
  
- (recommended but optional) Add to Task Scheduler or equivalent (put the executable in `shell:common startup` in Windows Explorer) to run on startup

This runs the script on startup and in the background.
Enable this if you use Task Scheduler else TTS will not work:

![Run only when user is logged on (checked)](image.png)

You can run the Python script from cloning or the executable from releases, **but make sure to have `config.json` in the same directory**.

Note: when using `actions.PlaySound`, remember to add the sound files to `AntiProcrastinator.spec` if using Pyinstaller.