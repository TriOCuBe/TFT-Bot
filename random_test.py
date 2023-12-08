import mss.tools
import numpy
from pytesseract import pytesseract
from time import sleep
import cv2
from tft_bot.helpers import system_helpers
from tft_bot import config

bounding_box = (
    1415,
    265,
    1550,
    295
)

print("taking ss in 5 seconds")
sleep(5)
with mss.mss() as ss_taker:
    screenshot = ss_taker.grab(bounding_box)
    mss.tools.to_png(screenshot.rgb, screenshot.size, output="image.png")

pixels = numpy.array(screenshot)
gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)

del screenshot
del pixels

_TESSERACT_CONFIG = '--oem 3 --psm 7 -c tessedit_char_whitelist=abcdefghjklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c page_separator=""'
config.load_config(r".\output")
pytesseract.tesseract_cmd = config.get_tesseract_location(system_helpers=system_helpers)
print(pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG))