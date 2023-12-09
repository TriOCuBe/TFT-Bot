import mss.tools
import numpy
from pytesseract import pytesseract
from time import sleep
import cv2
from tft_bot.helpers import system_helpers
from tft_bot import config

# resize_x = resize_y = 1

# bounding_box = (
#     int(1700 * resize_x),
#     int(325 * resize_y),
#     int(1860 * resize_x),
#     int(350 * resize_y),
# )

# print("taking ss in 5 seconds")
# sleep(5)
# with mss.mss() as ss_taker:
#     screenshot = ss_taker.grab(bounding_box)
#     mss.tools.to_png(screenshot.rgb, screenshot.size, output="image.png")

# pixels = numpy.array(screenshot)
# gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)

# del screenshot
# del pixels

# _TESSERACT_CONFIG = '--oem 3 --psm 7 -c tessedit_char_whitelist=abcdefghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c page_separator=""'
config.load_config(r".\output")
tesseract_location = config.get_tesseract_location(system_helpers=system_helpers)
# detected = pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG)

from tft_bot.helpers.screen_helpers import check_champion

champion = check_champion(tesseract_location=tesseract_location, wanted_traits=["mosher", "guardian"])

print(champion)
