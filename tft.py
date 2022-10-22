import pkg_resources
import pyautogui as auto
from python_imagesearch.imagesearch import imagesearch as search
import time
from printy import printy
import random
from datetime import datetime
import keyboard
import os
import psutil

pkg_resources.require("PyAutoGUI==0.9.50")
pkg_resources.require("opencv-python==4.6.0.66")
pkg_resources.require("python-imageseach-drov0==1.0.6")

CONSTANTS = {
    "executables": {
        "league": {
            "client": "C:\Riot Games\League of Legends\LeagueClient.exe",
            "game": "C:\Riot Games\League of Legends\Game\League of Legends.exe",
        },
    },
    "tft_logo": {
        "base": "./captures/tft_logo.png",
        "overshadowed": "./captures/tft_logo_overshadowed.png",
    },
    "client": {
        "pre_match": {
            "quick_play": "./captures/buttons/quick_play.png",
            "find_match_ready": "./captures/buttons/find_match_ready.png",
        },
        "in_queue": {
            "base": "./captures/buttons/in_queue.png",
            "overshadowed": "./captures/buttons/in_queue_overshadowed.png",
            "accept": "./captures/buttons/accept.png",
        },
        "dead": "./captures/dead.png",
        "reconnect": "./captures/buttons/reconnect.png",
        "post_game": {
            "skip_waiting_for_stats": "./captures/buttons/skip_waiting_for_stats.png",
            "play_again": "./captures/buttons/play_again.png",
            "missions_ok": "./captures/buttons/missions_ok.png",
        },
    },
    "game": {
        "loading": "./captures/loading.png",
        "exit_now": "./captures/buttons/exit_now.png",
        "settings": "./captures/buttons/settings.png",
        "surrender": {
            "surrender_1": "./captures/buttons/surrender_1.png",
            "surrender_2": "./captures/buttons/surrender_2.png",
        },
        "gamelogic": {
            "reroll": "./captures/buttons/reroll.png",
            "choose_one": "./captures/buttons/choose_one.png",
            "take_all": "./captures/buttons/take_all.png",
            "timer_1": "./captures/buttons/timer_1.png",
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

auto.FAILSAFE = False

global gamecount
global endtimer
gamecount = -1
endtimer = time.time()
pauselogic = False


def toggle_pause():
    global pauselogic
    print(
        f'alt+p pressed, toggling pause from {pauselogic} to {not pauselogic}')
    pauselogic = not pauselogic


keyboard.add_hotkey('alt+p', lambda: toggle_pause())

# Start utility methods


def onscreen(path, precision=0.8):
    return search(path, precision)[0] != -1


def search_to(path):
    pos = search(path)
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


def click_to(path, delay=.1):
    if onscreen(path):
        auto.moveTo(search(path))
        click_left(delay)
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
        except:
            # Nothing, we don't care
            continue
    return False


def league_already_running():
    return find_in_processes(CONSTANTS['executables']['league']['game'])

# Start between match logic


def queue():
    # Queue search loop
    while True:
        try:
            # Not already in queue
            if not is_in_queue():
                if is_in_tft_lobby():
                    print("TFT lobby detected, finding match")
                    click_to(CONSTANTS['client']['pre_match']['find_match_ready'])
                    time.sleep(3)
                elif league_already_running():
                    print("Already in game!")
                    break
                # Post-match screen
                elif check_if_post_game():
                    match_complete()
                else:
                    print("|WARN| TFT lobby not detected!")
                    time.sleep(60)

            #
            counter = 0
            while not onscreen(CONSTANTS['game']['loading']) and not onscreen(CONSTANTS['game']['round']['1-1']):
                time.sleep(1)
                click_to(CONSTANTS['client']['in_queue']['accept'])

                if not is_in_queue():
                    counter = counter + 1

                if (counter > 60):
                    print("Was not in queue for 60 seconds, abort?")
                    break

            if onscreen(CONSTANTS['game']['loading']):
                print("Loading!")
                break
            elif onscreen(CONSTANTS['game']['gamelogic']['timer_1']) or league_already_running():
                print("Already in game :O!")
                break
        except AttributeError:
            print("Not already in game, couldn't find game client on screen, looping")
            time.sleep(5)
            continue

    loading_match()


def loading_match():
    while not onscreen(CONSTANTS['game']['round']['1-1']) and not onscreen(CONSTANTS['game']['gamelogic']['timer_1']):
        time.sleep(1)

    print("Match starting!")
    start_match()


def start_match():
    while onscreen(CONSTANTS['game']['round']['1-1']):
        auto.moveTo(888, 376)
        click_right()

    print("In the match now!")
    main_game_loop()


def buy(iterations):
    for i in range(iterations):
        click_to(CONSTANTS['game']['trait']['bruiser'])
        click_to(CONSTANTS['game']['trait']['mage'])


def check_if_game_complete():
    if onscreen(CONSTANTS['client']['dead']):
        click_to(CONSTANTS['client']['dead'])
        time.sleep(5)
    return onscreen(CONSTANTS['client']['post_game']['play_again']) or onscreen(CONSTANTS['client']['pre_match']['quick_play'])


def attempt_reconnect_to_existing_game():
    if onscreen(CONSTANTS['client']['reconnect']):
        print("reconnecting!")
        time.sleep(0.5)
        click_to(CONSTANTS['client']['reconnect'])
        return False
    return True


def check_if_post_game():  # checks to see if game was interrupted
    if check_if_game_complete():
        return True
    return attempt_reconnect_to_existing_game()


def main_game_loop():
    exit = False
    while exit == False:
        if pauselogic:
            time.sleep(5)
        else:
            # Handle recurring round logic
            if onscreen(CONSTANTS['game']['round']['-4']):
                auto.moveTo(928, 396)
                click_right()
            elif onscreen(CONSTANTS['game']['round']['1-']) or onscreen(CONSTANTS['game']['round']['2-']):
                buy(3)
            # If round > 2, attempt re-rolls
            if not onscreen(CONSTANTS['game']['round']['1-']) and not onscreen(CONSTANTS['game']['round']['2-']):
                click_to(CONSTANTS['game']['gamelogic']['reroll'])
            time.sleep(1)

        if check_if_post_game():
            match_complete()
            break

    # Uncomment this (and change the round) if you'd like to surrender and lot let the match end automatically
    # if onscreen("./captures/2-5.png"):
    #     while not onscreen("./captures/3-1.png"):  # change this if you want to surrender at a different stage, also the image recognition struggles with 5 being it sees it as 3 so i had to do 6 as that's seen as a 5
    #         buy(5)
    #         click_to("./captures/reroll.png")
    #         time.sleep(1)
    #         checks()
    #     print("Surrendering now!")
    #     surrender()


def end_match():
    # added a main loop for the end match function to ensure you make it to the find match button.
    while not onscreen(CONSTANTS['client']['pre_match']['find_match_ready']):
        while onscreen(CONSTANTS['client']['post_game']['missions_ok']):
            print("Dismissing missions ok")
            click_to(CONSTANTS['client']['post_game']['missions_ok'])
            time.sleep(3)
        if onscreen(CONSTANTS['client']['post_game']['skip_waiting_for_stats']):
            print("Skipping waiting for stats")
            click_to(CONSTANTS['client']['post_game']['skip_waiting_for_stats'])
            time.sleep(10)
        if onscreen(CONSTANTS['client']['post_game']['play_again']):
            print("Attempting to play again")
            click_to(CONSTANTS['client']['post_game']['play_again'])
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

queue()

# End auth + main script
