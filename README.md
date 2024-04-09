# AntiProcrastinator

Your computer will yell at you for procrastinating.

Features:

-   Immediately yells at you on launch
-   Monitors the focused window and yells at you if you're procrastinating (configurable blacklist)
    -   Also pauses any music you're playing to yell at you
-   Regularly reminds you how close your exam(s) are (configurable)
-

## Usage:

-   Set the `exam_date` in `config.json`
-   Add any phrases you want to `blacklist` (e.g. discord, steam) for the focused window in `config.json`

Example:

```json
{
	"exam_date": "2024/05/09",
	"blacklist": ["discord", "playnite", "steam"]
}
```

-   (recommended) Add to Task Scheduler

This runs the script on startup and in the background.
Enable this else TTS will not work:

![Run only when user is logged on (checked)](image.png)
