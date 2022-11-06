import time
import logging
import pyautogui as auto
import python_imagesearch.imagesearch as imagesearch

from screen_helpers import onscreen, find_image
from better_image_click import click_image_rand
import generic_helpers

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
        try:
            auto.moveTo(imagesearch.imagesearch(path))
            click_left(delay)
        except Exception as err:
            logging.debug(f"Failed to click to {err}")
    else:
        logging.debug(f"Could not find '{path}', skipping")

def click_to_multiple(images, conditional_func=None, delay=None):
    for image in images:
        try:
            click_to(image)
        except Exception:
            logging.debug(f"Failed to click {image}")
        if generic_helpers.is_var_number(delay):
            time.sleep(delay)
        if generic_helpers.is_var_function(conditional_func) and conditional_func():
            return True
    return False

def search_to(path):
    try:
        pos = imagesearch.imagesearch(path)
        if onscreen(path):
            auto.moveTo(pos)
            return pos
    except Exception:
        return None

def click_to_middle(path, precision=0.8, delay=0.2, offset="half", action="left"):
    pos = find_image(path, precision)
    if pos:
        try:
            click_image_rand(path, pos, action, delay, offset=offset)
        except Exception as err:
            logging.debug(f"M|Failed to click to {err}")
    else:
        logging.debug(f"M|Could not find '{path}', skipping")

def click_to_middle_multiple(images, conditional_func=None, delay=None, action="left"):
    for image in images:
        try:
            click_to_middle(image, action=action)
        except Exception:
            logging.debug(f"M|Failed to click {image}")
        if generic_helpers.is_var_number(delay):
            time.sleep(delay)
        if generic_helpers.is_var_function(conditional_func) and conditional_func():
            return True
    return False