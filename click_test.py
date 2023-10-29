from tft_bot.helpers.click_helpers import move_to, click_to
from random import randint
from pyHM import mouse
import time

# time.sleep(5)

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

# screenshot = pyautogui.screenshot()
# screenshot_np = np.array(screenshot)
# screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
# result = cv2.matchTemplate(screenshot_rgb, cv2.imread(CONSTANTS["game"]["gamelogic"]["choose_an_augment"]), cv2.TM_CCOEFF_NORMED)
# _, _, _, max_loc = cv2.minMaxLoc(result)

# if result[max_loc[1], max_loc[0]] > 0.9:
#     click_to(960 * (10/12), 540 * (10/12))
#     print("found augment, clicking to middle")

# for _ in range(1):
#     # mouse.move(randint(0, 1600) + randint(0, 2), randint(0, 900) + randint(0, 2))
#     mouse.move(3000, 400)
#     time.sleep(0.1)

import mss
from pytesseract import pytesseract
from tft_bot.helpers import system_helpers
from tft_bot.config import get_tesseract_location

resize_x = 10/12
resize_y = 10/12

round_bounding_box = (
    int(league_bounding_box.min_x + (767 * resize_x)),
    int(league_bounding_box.min_y + (10 * resize_y)),
    int(league_bounding_box.min_x + (870 * resize_x)),
    int(league_bounding_box.min_y + (34 * resize_y)),
)
with mss.mss() as screenshot_taker:
    screenshot = screenshot_taker.grab(round_bounding_box)

pytesseract.tesseract_cmd = get_tesseract_location(system_helpers=system_helpers)

pixels = numpy.array(screenshot)
gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
game_round: str = pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG)

print(game_round)