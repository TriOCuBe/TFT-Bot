import cv2
import pyautogui
import random

def click_image_rand(image, pos, action, timestamp, offset="half"):
    img = cv2.imread(image)
    if img is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))
    height, width, channels = img.shape
    offset_to_use = min(height, width) / 2
    if offset != "half":
        offset_to_use = offset
    pyautogui.moveTo(pos[0] + r(width / 2, offset_to_use), pos[1] + r(height / 2, offset_to_use), timestamp)
    pyautogui.click(button=action)

def r(num, rand):
    return num + rand * random.random()