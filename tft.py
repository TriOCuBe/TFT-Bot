
import time
import random
import keyboard
import os

import argparse
import pkg_resources
import pyautogui as auto
import python_imagesearch.imagesearch as imagesearch
import psutil
from printy import printy
from datetime import datetime

import win32gui
import win32process
import win32con
import win32com.client

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.6.0.66")
pkg_resources.require("python-imagesearch==1.2.2")

arg_parser = argparse.ArgumentParser(prog="TFT Bot")
arg_parser.add_argument("--ffearly", action='store_true', help="If the game should be surrendered at first available time.")
arg_parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity, mostly useful for debugging")
parsed_args = arg_parser.parse_args()

FF_EARLY = parsed_args.ffearly
VERBOSE = parsed_args.verbose
if FF_EARLY:
    print("FF Early Specified - Will surrender at first available time")
else:
    print("FF Early Not Specified - Will play out games for their duration")

if VERBOSE:
    print("Will explain everything and be very verbose")
else:
    print("Will be quiet and not be very verbose")

CONSTANTS = {
    "executables": {
        "league": {
            "client": "C:\Riot Games\League of Legends\LeagueClient.exe",
            "client_ux": "C:\Riot Games\League of Legends\LeagueClientUx.exe",
            "game": "C:\Riot Games\League of Legends\Game\League of Legends.exe",
        },
    },
    "tft_logo": {
        "base": "./captures/tft_logo.png",
        "overshadowed": "./captures/tft_logo_overshadowed.png",
    },
    "client": {
        "screenshot_location": "./screenshots/",
        "pre_match": {
            "quick_play": "./captures/buttons/quick_play.png",
            "find_match": {
                "base": "./captures/buttons/find_match.png",
                "highlighted": "./captures/buttons/find_match_highlighted.png",
                "original": "./captures/buttons/find_match_original.png",
            }
        },
        "in_queue": {
            "base": "./captures/buttons/in_queue.png",
            "overshadowed": "./captures/buttons/in_queue_overshadowed.png",
            "accept": "./captures/buttons/accept.png",
        },
        "death": "./captures/death.png",
        "reconnect": "./captures/buttons/reconnect.png",
        "post_game": {
            "skip_waiting_for_stats": "./captures/buttons/skip_waiting_for_stats.png",
            "play_again": "./captures/buttons/play_again.png",
            "missions_ok": "./captures/buttons/missions_ok.png",
        },
    },
    "game": {
        "loading": "./captures/loading.png",
        "exit_now": {
            "base": "./captures/buttons/exit_now_base.png",
            "highlighted": "./captures/buttons/exit_now_highlighted.png",
        },
        "settings": "./captures/buttons/settings.png",
        "surrender": {
            "surrender_1": "./captures/buttons/surrender_1.png",
            "surrender_2": "./captures/buttons/surrender_2.png",
        },
        "gamelogic": {
            "choose_one": "./captures/buttons/choose_one.png",
            "reroll": "./captures/buttons/reroll.png",
            "take_all": "./captures/buttons/take_all.png",
            "timer_1": "./captures/timer_1.png",
            "xp_buy": "./captures/buttons/xp_buy.png",
        },
        "gold": {
            "0": "./captures/gold/0.png",
            "1": "./captures/gold/1.png",
            "2": "./captures/gold/2.png",
            "3": "./captures/gold/3.png",
            "4": "./captures/gold/4.png",
            "5": "./captures/gold/5.png",
            "6": "./captures/gold/6.png",
        },
        "round": {
            "-4": "./captures/round/-4.png",
            "1-": "./captures/round/1-.png",
            "2-": "./captures/round/2-.png",
            "1-1": "./captures/round/1-1.png",
            "2-2": "./captures/round/2-2.png",
            "2-3": "./captures/round/2-3.png",
            "2-4": "./captures/round/2-4.png",
            "2-5": "./captures/round/2-5.png",
            "3-1": "./captures/round/3-1.png",
            "3-2": "./captures/round/3-2.png",
            "3-3": "./captures/round/3-3.png",
            "3-4": "./captures/round/3-4.png",
            "3-7": "./captures/round/3-7.png",
            "4-6": "./captures/round/4-6.png",
            "4-7": "./captures/round/4-7.png",
            "6-5": "./captures/round/6-5.png",
            "6-6": "./captures/round/6-6.png",
        },
        "trait": {
            "astral": "./captures/trait/astral.png",
            "bruiser": "./captures/trait/bruiser.png",
            "chemtech": "./captures/trait/chemtech.png",
            "dragonmancer": "./captures/trait/dragonmancer.png",
            "jade": "./captures/trait/jade.png",
            "mage": "./captures/trait/mage.png",
            "scrap": "./captures/trait/scrap.png",
        },
    },
}

find_match_images = [
    CONSTANTS['client']['pre_match']['find_match']['base'],
    CONSTANTS['client']['pre_match']['find_match']['highlighted'],
    CONSTANTS['client']['pre_match']['find_match']['original'],
]

exit_now_images = [
    CONSTANTS['game']['exit_now']['base'],
    CONSTANTS['game']['exit_now']['highlighted'],
]

auto.FAILSAFE = False

global gamecount
global endtimer
gamecount = -1
endtimer = time.time()
pauselogic = False


def set_active_window(window_id):
    # Try to account for every scenario
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.BringWindowToTop(window_id)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)

def bring_window_to_forefront(window_title, path_to_verify=None):
    hwnd = win32gui.FindWindowEx(0,0,0, window_title)
    if (path_to_verify is not None):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        path = psutil.Process(pid).exe()
        if path != path_to_verify:
            print(f"Failed to find process to bring to forefront:\n\t{path} != {path_to_verify}")
            return
    set_active_window(hwnd)

def bring_league_client_to_forefront():
    bring_window_to_forefront("League of Legends", CONSTANTS['executables']['league']['client_ux'])

def toggle_pause():
    global pauselogic
    print(f'alt+p pressed, toggling pause from {pauselogic} to {not pauselogic}')
    pauselogic = not pauselogic
    if pauselogic:
        print("Bot now paused, remember to unpause to continue botting!")
    else:
        print("Bot playing again!")


keyboard.add_hotkey('alt+p', lambda: toggle_pause())

# Start utility methods
def onscreen(path, precision=0.8):
    return imagesearch.imagesearch(path, precision)[0] != -1

def onscreen_multiple_any(paths, precision=0.8):
    for path in paths:
        if (imagesearch.imagesearch(path, precision)[0] != -1):
            return True
    return False

def onscreen_region(path, x1, y1, x2, y2, precision=0.8):
    return imagesearch.imagesearcharea(path, x1, y1, x2, y2, precision)[0] != -1

def onscreen_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision=0.8):
    return imagesearch_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision)[0] != -1

# Via https://github.com/drov0/python-imagesearch/blob/master/python_imagesearch/imagesearch.py
def imagesearch_region_numLoop(image, timesample, maxSamples, x1, y1, x2, y2, precision=0.8):
    pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
    count = 0

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


def search_to(path):
    pos = imagesearch.imagesearch(path)
    if onscreen(path):
        auto.moveTo(pos)
        return pos


def click_key(key, delay=.1):
    auto.keyDown(key)
    time.sleep(delay)
    auto.keyUp(key)


def click_left(delay=.1):
    auto.mouseDown()
    time.sleep(delay)
    auto.mouseUp()


def click_right(delay=.1):
    auto.mouseDown(button='right')
    time.sleep(delay)
    auto.mouseUp(button='right')


def click_to(path, precision=0.8, delay=.1):
    if onscreen(path, precision):
        auto.moveTo(imagesearch.imagesearch(path))
        click_left(delay)
    else:
        print(f"Could not find '{path}', skipping")

def click_to_multiple(images, conditional_func=None, delay=None):
    for image in images:
        try:
            click_to(image)
        except Exception:
            print(f"Failed to click {image}")
        if is_var_number(delay):
            time.sleep(delay)
        if is_var_function(conditional_func) and conditional_func():
            return True
    return False

def is_var_number(var):
    try:
        return type(var) == int or type(var) == float
    except:
        pass
    return False

def is_var_function(var):
    try:
        return callable(var)
    except:
        pass
    return False

# End utility methods


def is_in_queue():
    return onscreen(CONSTANTS['client']['in_queue']['base']) or onscreen(CONSTANTS['client']['in_queue']['overshadowed'])


def is_in_tft_lobby():
    return onscreen(CONSTANTS['tft_logo']['base']) or onscreen(CONSTANTS['tft_logo']['overshadowed'])


def find_in_processes(executable_path):
    for proc in psutil.process_iter():
        try:
            if (proc.exe() == executable_path):
                return True
        except Exception:
            # Nothing, we don't care
            continue
    return False


def league_already_running():
    return find_in_processes(CONSTANTS['executables']['league']['game'])

def find_match():
    counter = 0
    bring_league_client_to_forefront()
    while is_in_tft_lobby():
        find_match_click_success = click_to_multiple(find_match_images, conditional_func=is_in_queue, delay=0.2)
        print(f"Clicking find match success: {find_match_click_success}")
        time.sleep(1)
        while not onscreen(CONSTANTS['game']['loading']) and not onscreen(CONSTANTS['game']['round']['1-1']) and is_in_queue():
            click_to(CONSTANTS['client']['in_queue']['accept'])
            time.sleep(1)

            if not is_in_queue():
                counter = counter + 1

            if (counter > 60):
                print("Was not in queue for 60 seconds, aborting")
                break

# Start between match logic
def queue():
    # Queue search loop
    while True:
        # Not already in queue
        if not is_in_queue():
            if is_in_tft_lobby():
                print("TFT lobby detected, finding match")
                find_match()
            elif league_already_running():
                print("Already in game!")
                break
            # Post-match screen
            elif check_if_post_game():
                match_complete()
            else:
                print("|WARN| TFT lobby not detected!")
                time.sleep(5)

        #

        if onscreen(CONSTANTS['game']['loading']):
            print("Loading!")
            break
        elif onscreen(CONSTANTS['game']['gamelogic']['timer_1']) or league_already_running():
            print("Already in game :O!")
            break
    loading_match()

def loading_match():
    while not onscreen(CONSTANTS['game']['round']['1-1']) and not onscreen(CONSTANTS['game']['gamelogic']['timer_1']):
        time.sleep(1)

    print("Match starting!")
    start_match()


def start_match():
    while onscreen(CONSTANTS['game']['round']['1-1']):
        shared_draft_pathing()

    print("In the match now!")
    main_game_loop()

def shared_draft_pathing():
    auto.moveTo(946, 315)
    click_right()
    time.sleep(3)
    auto.moveTo(700, 450)
    click_right()
    time.sleep(3)
    auto.moveTo(950, 675)
    click_right()
    time.sleep(3)
    auto.moveTo(1200, 460)
    click_right()

def buy(iterations):
    for i in range(iterations):
        if check_if_gold_at_least(1):
            click_to(CONSTANTS['game']['trait']['bruiser'])
            time.sleep(0.5)
            click_to(CONSTANTS['game']['trait']['mage'])
            time.sleep(0.5)
            click_to(CONSTANTS['game']['trait']['jade'])
            time.sleep(0.5)
        time.sleep(0.5)

def exit_now_conditional():
    return not league_already_running()

def check_if_game_complete():
    if onscreen(CONSTANTS['client']['death']):
        print("Death detected")
        click_to(CONSTANTS['client']['death'])
        time.sleep(5)
    if onscreen_multiple_any(exit_now_images):
        print("End of game detected")
        exit_now_bool = click_to_multiple(exit_now_images, conditional_func=exit_now_conditional, delay=1.5)
        print(f"Exit now clicking success: {exit_now_bool}")
        time.sleep(5)
    return onscreen(CONSTANTS['client']['post_game']['play_again']) or onscreen(CONSTANTS['client']['pre_match']['quick_play'])


def attempt_reconnect_to_existing_game():
    if onscreen(CONSTANTS['client']['reconnect']):
        print("Reconnecting!")
        time.sleep(0.5)
        click_to(CONSTANTS['client']['reconnect'])
    return False


def check_if_post_game():  # checks to see if game was interrupted
    if check_if_game_complete():
        return True
    return attempt_reconnect_to_existing_game()

def check_if_gold_at_least(num):
    print(f"Looking for at least {num} gold")
    for i in range(num + 1):
        # print(f"Checking for {i} gold")
        try:
            if onscreen_region_numLoop(CONSTANTS['game']['gold'][f"{i}"], 0.1, 5, 780, 850, 970, 920, 0.9):
                print(f"Found {i} gold")
                if (i == num):
                    print("Correct")
                    return True
                else:
                    print("Incorrect")
                    return False
        except Exception:
            print(f"Exception finding {i} gold")
            # We don't have this gold as a file
            return True
    return True

def main_game_loop():
    exit = False
    while exit == False:
        if pauselogic:
            time.sleep(5)
        else:
            # Handle recurring round logic
            # Treasure dragon, dont reroll just take it
            if onscreen(CONSTANTS['game']['gamelogic']['take_all']):
                click_to(CONSTANTS['game']['gamelogic']['take_all'])
                time.sleep(1)
                continue
            # Free champ round
            if not onscreen(CONSTANTS['game']['round']['1-'], 0.9) and onscreen(CONSTANTS['game']['round']['-4'], 0.9):
                print("Round X-4, draft detected")
                shared_draft_pathing()
                continue
            elif onscreen(CONSTANTS['game']['round']['1-'], 0.9) or onscreen(CONSTANTS['game']['round']['2-'], 0.9):
                buy(3)
            # If round > 2, attempt re-rolls
            if check_if_gold_at_least(4) and onscreen(CONSTANTS['game']['gamelogic']['xp_buy']):
                click_to(CONSTANTS['game']['gamelogic']['xp_buy'])
                time.sleep(1)
                continue
            if not onscreen(CONSTANTS['game']['round']['1-'], 0.9) and not onscreen(CONSTANTS['game']['round']['2-'], 0.9):
                if check_if_gold_at_least(2) and onscreen(CONSTANTS['game']['gamelogic']['reroll']):
                    click_to(CONSTANTS['game']['gamelogic']['reroll'])

            time.sleep(1)

        if check_if_post_game():
            match_complete()
            break

        if FF_EARLY:
            # Change the round to end the round early at a different time
            # change this if you want to surrender at a different stage, also the image recognition struggles with 5 being it sees it as 3 so i had to do 6 as that's seen as a 5
            if not onscreen(CONSTANTS["game"]["1-"], 0.9) and not onscreen(CONSTANTS["game"]["2-", 0.9]):
                if not onscreen("./captures/3-1.png", 0.9):
                    print("Surrendering now!")
                    surrender()
                    break


def end_match():
    # added a main loop for the end match function to ensure you make it to the find match button.
    while not onscreen_multiple_any(find_match_images):
        while onscreen(CONSTANTS['client']['post_game']['missions_ok']):
            print("Dismissing mission")
            #screenshot if you have an "ok" button
            t = time.localtime()    # added for printing time
            current_time = time.strftime("%H%M%S", t) #for the changing file name
            myScreenshot = auto.screenshot()
            myScreenshot.save(rf'{CONSTANTS["client"]["screenshot_location"]}/{current_time}.png')
            time.sleep(2)
            print("SS saved")
            click_to(CONSTANTS['client']['post_game']['missions_ok'])
            time.sleep(3)
        if onscreen(CONSTANTS['client']['post_game']['skip_waiting_for_stats']):
            print("Skipping waiting for stats")
            click_to(CONSTANTS['client']['post_game']['skip_waiting_for_stats'])
            time.sleep(10)
        if onscreen(CONSTANTS['client']['post_game']['play_again']):
            print("Attempting to play again")
            bring_league_client_to_forefront()
            click_to(CONSTANTS['client']['post_game']['play_again'], delay=0.5)
            time.sleep(3)
        if onscreen(CONSTANTS['client']['pre_match']['quick_play']):
            print("Attempting to quick play")
            click_to(CONSTANTS['client']['pre_match']['quick_play'])
            time.sleep(10)


def match_complete():
    print_timer()
    print("Match complete! Cleaning up and restarting")
    time.sleep(3)
    end_match()


def surrender():
    counter = 0
    surrenderwait = random.randint(100, 150)
    print(f'Waiting {surrenderwait} seconds ({surrenderwait / 60 } minutes) to surrender')
    time.sleep(surrenderwait)
    print("Starting surrender")
    click_to(CONSTANTS['game']['settings'])

    while not onscreen(CONSTANTS['game']['surrender']['surrender_1']):
        # just in case it gets interrupted or misses
        click_to(CONSTANTS['game']['settings'])
        time.sleep(1)
        counter = counter + 1
        if (counter > 20):
            break
    counter = 0
    while not onscreen(CONSTANTS['game']['surrender']['surrender_2']):
        click_to(CONSTANTS['game']['surrender']['surrender_1'])
        # added a check here for the rare case that the game ended before the surrender finished.
        if check_if_post_game():
            return
        counter = counter + 1
        if (counter > 20):
            break

    time.sleep(1)
    click_to(CONSTANTS['game']['surrender']['surrender_2'])
    time.sleep(10)
    end_match()
    time.sleep(5)

    print("Surrender Complete")
    match_complete()


def print_timer():
    global endtimer
    endtimer = time.time()
    global gamecount
    gamecount += 1
    sec = (endtimer - starttimer)
    hours = sec // 3600
    sec = sec - hours*3600
    mu = sec // 60
    ss = sec - mu*60
    gamecount_string = str(gamecount)
    #result_list = str(datetime.timedelta(seconds=sec)).split(".")
    print("-------------------------------------")
    print("Current Time =", datetime.now().strftime("%H:%M:%S"))
    print("-------------------------------------")
    print("Game End")
    print("Play Time : ", int(float(hours)), "Hour", int(float(mu)), "Min", int(float(ss)), "Sec")
    print("Gamecount : ", gamecount_string)
    print("-------------------------------------")
    print("End of printing timer!")
# End main process


os.system('color 0F')
# Start auth + main script
print("Initial codebase by:")
printy(r"""
[c>] _____       _                            _   @
[c>]|  __ \     | |                          | |  @
[c>]| |  | | ___| |_ ___ _ __ __ _  ___ _ __ | |_ @
[c>]| |  | |/ _ \ __/ _ \ '__/ _` |/ _ \ '_ \| __|@
[c>]| |__| |  __/ ||  __/ | | (_| |  __/ | | | |_ @
[c>]|_____/ \___|\__\___|_|  \__, |\___|_| |_|\__|@
[c>]                          __/ |               @
[c>]                         |___/                @
""", "{k}")
print("Re-written by:")
printy(r"""
[c>]    __ __              __              __                __                  __  @
[c>]   / //_/__  __ _____ / /__  __ _____ / /__ ___   _____ / /_   __  __ _____ / /__@
[c>]  / ,<  / / / // ___// // / / // ___// //_// _ \ / ___// __ \ / / / // ___// //_/@
[c>] / /| |/ /_/ // /   / // /_/ // /__ / ,<  /  __// /__ / / / // /_/ // /__ / ,<   @
[c>]/_/ |_|\__, //_/   /_/ \__,_/ \___//_/|_| \___/ \___//_/ /_/ \__,_/ \___//_/|_|  @
[c>]      /____/                                                                     @
""", "{k}")

printy(f"Welcome! \nPlease feel free to ask questions or contribute at https://github.com/Kyrluckechuck/tft-bot", "nB{k}")
auto.alert("Press OK when you're in a TFT lobby!\n")
printy("Bot started, queuing up!", "w{k}")
os.system('color 0F')
global starttimer
starttimer = time.time()

def tft_bot_loop():
    while True:
        try:
            queue()
        except AttributeError:
            print("Not already in game, couldn't find game client on screen, looping")
            time.sleep(5)
            continue

tft_bot_loop()
