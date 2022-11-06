import cv2
import pyautogui as auto
import random
import logging
import time

def click_image_rand(image, pos, action, move_duration, offset="half", delay=0.1):
    img = cv2.imread(image)
    if img is None:
        logging.debug('Image file not found: {}'.format(image))
        return False
    height, width, channels = img.shape
    offset_to_use = min(height, width) / 2
    if offset != "half":
        offset_to_use = offset
    auto.moveTo(pos[0] + r(width / 2, offset_to_use), pos[1] + r(height / 2, offset_to_use), move_duration)
    click_action(delay=delay, button=action)
    return True

def click_action(delay=.1, button="left"):
    auto.mouseDown(button=button)
    time.sleep(delay)
    auto.mouseUp(button=button)

def r(num, rand):
    return num + rand * random.random()