# Python TFT Auto Battler Bot

This is an auto TFT bot, with some decent logic built in.

Some features of this bot:
- Ability to pause while it's evaluating the in-game event loop using `alt+p`
  - This uses the [keyboard](https://pypi.org/project/keyboard/) package, which allows it to listen globally (so you don't need to have the console selected in the foreground for this to take effect)
- Does not surrender, allowing it to play out most games, which at the ELO your bot will end up at means there's a decent chance you end up in top 4
  - If you're using this for event pass grinding, it will increase your odds of being top 4 which increases the points earned per minute played
- 

Some features I hope to implement at some point:
- Ability to work on any monitor and/or in Windowed mode (make clicking relative to window location), which would help in not needing to change your actual monitors resolution

## Info / Why I forked it
I've fairly heavily forked this from what it originally was, but if you'd like to see the original, I'm not claiming to have made this from scratch:

- https://github.com/Detergent13

I decided to fork this after being frustrated with the lack of updates and/or features, and the delay it would take in getting PRs merged even if the work is done by the community. I had been using this modified script for a while now, but realized I may as well formally fork & upload it since it's been fairly stable.

To be clear I don't blame Detergent13 at all, I just have different feelings about what belongs in the bot / envisions for what this could become.

On that note, if anyone has any suggestions / features they would like to see, please feel free to suggest in an [issue](https://github.com/Kyrluckechuck/tft-bot/issues), or by submitting your own PR to this!

# Installation:

* Install Python 3.8.3 from [here](https://www.python.org/downloads/), or the Windows Store
* Navigate to your install directory using `cd` and run `pip install -r requirements.txt` in Command Prompt
* Navigate to your install directory using `cd` and run `py "tft.py"` in Command Prompt
* Follow the instructions in your terminal window! Get into a TFT lobby, have the created window visible on your screen, and press 'OK' to start the bot!

# Troubleshooting:

* If these steps don't work, try running the file with `python "tft.py"` instead (For Windows Store/MacOS/Linux users especially) Likewise, try `pip3` instead of `pip` for installing requirements.
* If pip doesn't seem to exist, try installing it [here](https://pip.pypa.io/en/stable/installing/). Essentially 'save as' from [here](https://bootstrap.pypa.io/get-pip.py), then run `py get-pip.py` and try to use pip again
* The bot is configured to work with in-game resolution 1920x1080, and League client resolution 1280x720. (Also Windows scaling 100%) You can switch this up though, just re-capture the images in the captures folder!
* If you're having issues with Python not working properly, please make sure you have the correct version (3.8.3) installed, and all of the correct module versions installed, as listed in requirements.txt
* Make sure to run League and the bot on your main monitor, as it doesn't support additional monitors!
If you need additional help, feel free to reach out to me via an [issue](https://github.com/Kyrluckechuck/tft-bot/issues).
