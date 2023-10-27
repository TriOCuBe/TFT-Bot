from tft_bot.helpers.click_helpers import move_to, click_to
from random import randint
from pyHM import mouse
import time

time.sleep(5)

# mouse.down()
# for _ in range(10):
#     move_to(randint(100,1800), randint(100,900))
#     time.sleep(0.3)
#     # click_to(randint(400,1600), randint(200,700), action="right")
# mouse.up()
# click_to(960 * (10/12), 540 * (10/12), action="right")

import pyautogui
import cv2
import numpy as np
from tft_bot.constants import CONSTANTS

screenshot = pyautogui.screenshot()
screenshot_np = np.array(screenshot)
screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
result = cv2.matchTemplate(screenshot_rgb, cv2.imread(CONSTANTS["game"]["gamelogic"]["choose_an_augment"]), cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(result)

if result[max_loc[1], max_loc[0]] > 0.9:
    click_to(960 * (10/12), 540 * (10/12))
    print("found augment, clicking to middle")