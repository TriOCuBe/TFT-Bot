"""A collection of click helpers."""
import random
import time
import keyboard
from pyHM import mouse

from tft_bot.helpers.screen_helpers import ImageSearchResult


def click(delay=0.1, button="left") -> None:
   
    """A click helper to simulate clicking the specified button.

    Args:
        delay (float, optional): The delay between button down & up. Defaults to .1.
        button (str, optional): Button of the mouse to activate : "left" "right" "middle",
            see pyautogui.click documentation for more info. Defaults to "left".
    """
    if button == "right":
        # holding a button allows right clicks to move the character even when clicking on a champion. This way we ensure that we actually move to the points.
        keyboard.press('S')
    
    mouse.down(button=button)
    time.sleep(delay)
    mouse.up(button=button)
    
    if button == "right":
        keyboard.release('S')


def move_to(
    position_x: int,
    position_y: int,
) -> None:
    """
    Move the mouse to a specific position on the screen

    Args:
        position_x: The x coordinate to move to
        position_y: The y coordinate to move to
    """
    # auto.moveTo(position_x, position_y, random.uniform(0.4, 1.1))
    position_x = position_x + random.randint(0, 2)
    position_y = position_y + random.randint(0, 2)
    mouse.move(position_x, position_y, multiplier=0.6)


def click_to(
    position_x: int,
    position_y: int,
    delay: float = 0.1,
    action: str = "left",
) -> None:
    """
    Click to a specific position on the screen

    Args:
        position_x: The x coordinate to click to
        position_y: The y coordinate to click to
        delay (float, optional): The delay between mouse down & up. Defaults to 0.2.
        action (str, optional): The mouse button to perform. Defaults to "left".
    """
    # auto.moveTo(position_x, position_y, random.uniform(0.4, 1.1))
    move_to(position_x, position_y)
    click(delay=delay, button=action)
    # if action == "left":
    #     mouse.click(position_x, position_y)
    # else:
    #     mouse.right_click(position_x, position_y)


def click_to_image(
    image_search_result: ImageSearchResult | None,
    delay: float = 0.2,
    action: str = "left",
) -> bool:
    """
    Attempt to click to a specified image.

    Args:
        image_search_result: The result of an image search (screen_helpers.get_on_screen)
        delay: The delay between mouse down & up. Defaults to 0.2.
        action: The mouse button to perform. Defaults to "left".

    Returns:
        True if we had an image to click to, False if not
    """
    if not image_search_result:
        return False

    quarter_x = int(image_search_result.width / 4)
    quarter_y = int(image_search_result.height / 4)
    offset_x = random.randint(quarter_x, quarter_x * 3)
    offset_y = random.randint(quarter_y, quarter_y * 3)

    click_to(
        position_x=image_search_result.position_x + offset_x,
        position_y=image_search_result.position_y + offset_y,
        delay=delay,
        action=action,
    )
    return True


def hold_and_move_to(position_x: int, position_y: int, action: str = "left"):
    """
    Holds down a mouse button and moves the cursor to coordinates, then stops holding.

    Args:
        position_x: The x coordinate to move to.
        position_y: The y coordinate to move to.
        action: The mouse button to perform. Defaults to "left".
    """
    mouse.down(button=action)
    time.sleep(0.1)
    move_to(position_x, position_y)
    time.sleep(0.1)
    mouse.up(button=action)

def press(key: str) -> None:
    """
    Presses a key.

    Args:
        key: The key to press.
    """
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)