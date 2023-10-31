"""A collection of screen helpers for detecting when images are on screen."""
from dataclasses import dataclass

import cv2
from loguru import logger
import mss
import numpy
from pytesseract import pytesseract
import win32gui
from difflib import SequenceMatcher

from tft_bot.constants import CONSTANTS


@dataclass
class BoundingBox:
    """
    A dataclass holding information about a bounding box, a rectangle of two coordinate sets.
    """

    min_x: int
    min_y: int
    max_x: int
    max_y: int

    def to_tuple(self) -> tuple[int, int, int, int]:
        """
        Converts the bounding box to a tuple.

        Returns:
            A tuple, ordered min_x, min_y, max_x, max_y.

        """
        return self.min_x, self.min_y, self.max_x, self.max_y

    def get_width(self) -> int:
        """
        Get the width of the bounding box.

        Returns:
            The width as an integer.
        """
        return self.max_x - self.min_x

    def get_height(self) -> int:
        """
        Get the height of the bounding box.

        Returns:
            The height as an integer.
        """
        return self.max_y - self.min_y


@dataclass
class Coordinates:
    """
    A dataclass holding information about offset pixels to click to.
    """

    position_x: int
    position_y: int


@dataclass
class ImageSearchResult(Coordinates):
    """
    A dataclass holding information about an image search result.
    """

    width: int
    height: int


def get_window_bounding_box(window_title: str) -> BoundingBox | None:
    """
    Gets the bounding box of a specific window.

    Returns:
        A bounding box (min x, min y, max x, max y) or None if no window exists.

    """
    league_game_window_handle = win32gui.FindWindowEx(0, 0, 0, window_title)
    if not league_game_window_handle:
        logger.debug(f"We tried to check {window_title} for an image, but there is no window")
        return None

    return BoundingBox(*win32gui.GetWindowRect(league_game_window_handle))


def check_league_game_size(log: bool = True) -> tuple | None:
    """
    Check the league game size and print an error if it is not what we need it to be.

    Args:
        log: If you want to use this outside of init, set this to False. It will then return a tuple of the game's size

    Returns:
        If log is False, returns a tuple of the game's size in the format (width, height) 
    """
    league_game_bounding_box = get_window_bounding_box(window_title="League of Legends (TM) Client")
    if not league_game_bounding_box:
        return
        
    width = league_game_bounding_box.get_width()
    height = league_game_bounding_box.get_height()

    if log:
        if (width != 1920 and height != 1080) or (width != 1600 and height != 900):
            logger.error(
                f"Your game's size is {width} x {height} "
                f"instead of 1920 x 1080 or 1600 x 900! This WILL cause issues!"
            )
    else:
        return (width, height)


def calculate_window_click_offset(window_title: str, position_x: int, position_y: int) -> Coordinates | None:
    """
    Calculate absolute screen coordinates based off relative pixel position in a specific window.
    For game and client: If window size is not 1920x1080 or 1280x720 respectively, manipulate given x and y values

    Args:
        window_title: The title of the window to click in.
        position_x: The relative x coordinate to click to.
        position_y: The relative y coordinate to click to.

    Returns:
        Absolute coordinates to click to.
    """
    window_bounding_box = get_window_bounding_box(window_title=window_title)
    if not window_bounding_box:
        return None
    
    if window_title == CONSTANTS["window_titles"]["game"]:
        resize = True
        original_x = 1920
        original_y = 1080
    elif window_title == CONSTANTS["window_titles"]["client"]:
        resize = True
        original_x = 1280
        original_y = 720

    if resize:
        resize_x = window_bounding_box.get_width() / original_x
        resize_y = window_bounding_box.get_height() / original_y
        position_x = int(position_x * resize_x)
        position_y = int(position_y * resize_y)


    return Coordinates(
        position_x=window_bounding_box.min_x + position_x, position_y=window_bounding_box.min_y + position_y
    )


def get_on_screen_in_client(
    path: str, precision: float = 0.8, offsets: BoundingBox | None = None
) -> ImageSearchResult | None:
    """
    Check if a given image is detected on screen, but only check the league client window.

    Args:
        path: The relative or absolute path to the image to be found.
        precision: The precision to be used when matching the image. Defaults to 0.8.
        offsets: A bounding box to off-set the region by. Useful if you only want to check a specific region.
          Defaults to None.

    Returns:
        The position of the image and it's width and height or None if it wasn't found
    """
    return get_on_screen(
        window_title=CONSTANTS["window_titles"]["client"], path=path, precision=precision, offsets=offsets
    )


def get_on_screen_in_game(
    path: str, precision: float = 0.8, offsets: BoundingBox | None = None
) -> ImageSearchResult | None:
    """
    Check if a given image is detected on screen, but only check the league game window.

    Args:
    path: The relative or absolute path to the image to be found.
    precision: The precision to be used when matching the image. Defaults to 0.8.
    offsets: A bounding box to off-set the region by. Useful if you only want to check a specific region. Defaults to None.

    Returns:
    The position of the image and it's width and height or None if it wasn't found
    """
    return get_on_screen(
        window_title=CONSTANTS["window_titles"]["game"], path=path, precision=precision, offsets=offsets
    )


def get_on_screen(
    window_title: str, path: str, precision: float = 0.8, offsets: BoundingBox | None = None
) -> ImageSearchResult | None:
    """
    Check if a given image is detected on screen in a specific window's area.

    Args:
    window_title: The title of the window we should look at.
    path: The relative or absolute path to the image to be found.
    precision: The precision to be used when matching the image. Defaults to 0.8.
    offsets: A bounding box to off-set the region by. Useful if you only want to check a specific region. Defaults to None.

    Returns:
    The position of the image and it's width and height or None if it wasn't found
    """
    window_bounding_box = get_window_bounding_box(window_title=window_title)
    if not window_bounding_box:
        return None

    image_to_find = cv2.imread(path, 0)
    if image_to_find is None:
        logger.warning(f"The image {path} does not exist on the system or we do not have permission to read it")
        return None

    if offsets:
        width = window_bounding_box.get_width()
        height = window_bounding_box.get_height()

        resize_x = 1
        resize_y = 1
        if window_title == CONSTANTS["window_titles"]["game"]:
            resize_x = width / 1920
            resize_y = height / 1080
        elif window_title == CONSTANTS["window_titles"]["client"]:
            resize_x = width / 1280
            resize_y = height / 720

        window_bounding_box.min_x += int(offsets[0] * resize_x)
        window_bounding_box.min_y += int(offsets[1] * resize_y)
        window_bounding_box.max_x += int(offsets[2] * resize_x)
        window_bounding_box.max_y += int(offsets[3] * resize_y)

    with mss.mss() as screenshot_taker:
        screenshot = screenshot_taker.grab(window_bounding_box.to_tuple())

    pixels = numpy.array(screenshot)
    gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    search_result = cv2.matchTemplate(gray_scaled_pixels, image_to_find, cv2.TM_CCOEFF_NORMED)

    _, max_precision, _, max_location = cv2.minMaxLoc(search_result)
    if max_precision < precision:
        return None

    return ImageSearchResult(
        position_x=max_location[0] + window_bounding_box.min_x,
        position_y=max_location[1] + window_bounding_box.min_y,
        height=image_to_find.shape[0],
        width=image_to_find.shape[1],
    )


@logger.catch
def get_on_screen_multiple_any(window_title: str, paths: list[str], precision: float = 0.8) -> bool:
    """Check if any of the given images are detected on screen.

    Args:
        window_title: The title of the window we should look at.
        paths: The list of relative or absolute paths to images to be searched for.
        precision: The precision to be used when matching the image. Defaults to 0.8.

    Returns:
        True if any of the images are detected on screen, False otherwise.
    """
    for path in paths:
        if get_on_screen(window_title=window_title, path=path, precision=precision):
            return True

    return False


_TESSERACT_CONFIG = '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789 -c page_separator=""'


# essentially copied from https://github.com/jfd02/TFT-OCR-BOT/blob/ea3eb15d3f96109a616eb9f3508db14347ac0339/game_functions.py#L13
def get_round_with_ocr(tesseract_location) -> str | None:
    """
    Get the current round using ocr

    Args:
        tesseract_location: Required to initialize pytesseract. String of path to tesseract.exe

    Returns:
        The current round as a string or None if it can't identify anything
    """
    league_bounding_box = get_window_bounding_box(CONSTANTS["window_titles"]["game"])
    if not league_bounding_box:
        return 0

    width = league_bounding_box.get_width()
    height = league_bounding_box.get_height()
    min_x = league_bounding_box.min_x
    min_y = league_bounding_box.min_y

    resize_x = width / 1920
    resize_y = height / 1080

    with mss.mss() as screenshot_taker:
        round_bounding_box = (
            int(min_x + (767 * resize_x)),
            int(min_y + (10 * resize_y)),
            int(min_x + (870 * resize_x)),
            int(min_y + (34 * resize_y)),
        )
        screenshot = screenshot_taker.grab(round_bounding_box)    

    pytesseract.tesseract_cmd = tesseract_location

    pixels = numpy.array(screenshot)
    gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    game_round: str = pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG)

    # i dont fucking know why i need to do this, but it wont work otherwise. is pytesseract returning some invisible symbol???
    if game_round != '':
        game_round = int(game_round)
        game_round = str(game_round)

    if game_round in CONSTANTS["game"]["round_text"]:
        logger.debug(f"OCR recognized current round as {game_round[0]}-{game_round[1]}")
        return game_round
    
    return None

def get_gold_with_ocr() -> int:
    """
    Get the gold by taking a screenshot of the region where it is and running OCR over it.
    This should only be called by ocr_* implementations in the economy package, since they set where Tesseract-OCR is.

    Returns:
        The amount of gold the player currently has.
    """
    league_bounding_box = get_window_bounding_box(CONSTANTS["window_titles"]["game"])
    if not league_bounding_box:
        return 0

    width = league_bounding_box.get_width()
    height = league_bounding_box.get_height()

    resize_x = width / 1920
    resize_y = height / 1080

    gold_bounding_box = (
        int(league_bounding_box.min_x + (867 * resize_x)),
        int(league_bounding_box.min_y + (881 * resize_y)),
        int(league_bounding_box.min_x + (924 * resize_x)),
        int(league_bounding_box.min_y + (909 * resize_y)),
    )
    with mss.mss() as screenshot_taker:
        screenshot = screenshot_taker.grab(gold_bounding_box)

    pixels = numpy.array(screenshot)
    gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    return int(pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG) or 0)


def get_gold_with_opencv(num: int) -> bool:
    """
    Checks if there is N gold in the region of the gold display.

    Args:
        num: The amount of gold we're checking for, there should be a file for it in captures/gold .

    Returns:
        True if we found the amount of gold. False if not.
    """
    try:
        if get_on_screen_in_game(CONSTANTS["game"]["gold"][f"{num}"], 0.9, BoundingBox(int(780 * (10/12)), int(850 * (10/12)), int(970 * (10/12)), int(920*  (10/12)))):
            logger.debug(f"Found {num} gold")
            return True
    except Exception as exc:
        logger.opt(exception=exc).debug(f"Exception finding {num} gold, we possibly don't have the value as a file")
        # We don't have this gold as a file
        return True
    return False


def gold_at_least(num: int) -> bool:
    """
    Check if the gold on screen is at least the provided amount with opencv

    Args:
        num (int): The value to check if the gold is at least.

    Returns:
        bool: True if the value is >= `num`, False otherwise.
    """
    logger.debug(f"Looking for at least {num} gold")
    if get_gold_with_opencv(num):
        return True

    for i in range(num + 1):
        if get_gold_with_opencv(i):
            return i >= num

    logger.debug("No gold value found, assuming we have more")
    return True


# H, S, V
LOWER_GREEN = numpy.array([40, 150, 10])
UPPER_GREEN = numpy.array([75, 255, 255])

FIELD_SLOT_Y_POSITIONS = numpy.array([672, 596, 515, 446])
MINIMUM_Y_OFFSET = 75


def get_board_positions() -> list[Coordinates]:
    """
    Get position of units on the board.

    Returns: A list of coordinates holding the board position of the unit.
    """
    window_bounding_box = get_window_bounding_box(window_title=CONSTANTS["window_titles"]["game"])
    if not window_bounding_box:
        return []

    with mss.mss() as screenshot_taker:
        screenshot = screenshot_taker.grab(window_bounding_box.to_tuple())

    pixels = numpy.array(screenshot)
    hsv_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_pixels, LOWER_GREEN, UPPER_GREEN)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    positions = []
    for contour in contours:
        position_x, position_y, width, height = cv2.boundingRect(contour)

        if position_y < int(275 * (10/12)) or position_y > int(672 * (10/12)):
            continue

        if width < int(55 * (10/12)) or width > int(80 * (10/12)) or height < int(5 * (10/12)) or height > int(20 * (10/12)):
            continue

        position_x = int(position_x + (width / 2))
        position_y = int(position_y + (height / 2)) + MINIMUM_Y_OFFSET
        potential_unit_y_positions = FIELD_SLOT_Y_POSITIONS[FIELD_SLOT_Y_POSITIONS > position_y]
        if len(potential_unit_y_positions) == 0:
            continue

        positions.append(Coordinates(position_x=position_x, position_y=potential_unit_y_positions.min()))

    return positions


# essentially copied from https://github.com/jfd02/TFT-OCR-BOT/blob/main/arena_functions.py#L118
def valid_item(item: str) -> str | None:
    """
    Checks if given item name is valid or not

    Args:
        item: A string of the item name to check

    Returns:
        String of item or None
    """
    return next(
        (
            valid_name
            for valid_name in CONSTANTS["game"]["items"]
            if valid_name in item or SequenceMatcher(a=valid_name, b=item).ratio() >= 0.7
        ),
        None,
    )

_TESSERACT_CONFIG_ITEMS = '--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -c page_separator=""'

def get_items() -> list:
    """
    Checks every position for items and looks if there is one present.

    Returns:
        List of dictionaries, with tuple "coordinates" and string "item_name".
    """
    from tft_bot.helpers.click_helpers import move_to

    league_bounding_box = get_window_bounding_box(CONSTANTS["window_titles"]["game"])
    if not league_bounding_box:
        return 0

    width = league_bounding_box.get_width()
    height = league_bounding_box.get_height()

    resize_x = width / 1920
    resize_y = height / 1080

    item_list = []
    for pos in CONSTANTS["game"]["coordinates"]["items"]:
        offset = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=pos[0], position_y=pos[1]
        )
        move_to(position_x=offset.position_x, position_y=offset.position_y)
        
        # commented out since it wasn't very reliable
        # item_box = (
        #     int(offset.position_x + (100 * resize_x)),
        #     int(offset.position_y + (40 * resize_y)),
        #     int(offset.position_x + (240 * resize_x)),
        #     int(offset.position_y + (70 * resize_y)),
        # )

        # with mss.mss() as screenshot_taker:
        #     screenshot = screenshot_taker.grab(item_box)

        # pixels = numpy.array(screenshot)
        # gray_scaled_pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
        # item_name = pytesseract.image_to_string(~gray_scaled_pixels, config=_TESSERACT_CONFIG_ITEMS)

        # item_list.append({"coordinates": (offset.position_x, offset.position_y), "item_name": valid_item(item_name)})

        if get_on_screen_in_game(CONSTANTS["game"]["gamelogic"]["recipe"]) or get_on_screen_in_game(CONSTANTS["game"]["gamelogic"]["emblem"]):
            item_list.append((offset.position_x, offset.position_y))
        else:
            item_list.append(None)

    logger.debug(f"Found items at: {item_list}")
    return item_list

def check_champion(wanted_traits: list) -> str | None:
    """
    Checks if and what champion is displayed on the right-hand side of the screen. Should be used in combination with clicking to bench or board slot.

    Args:
    wanted_traits: List of traits we are searching for.

    Returns:
    Name of detected champ as string or None if nothing was found. (Currently only void and sorcerer champs can be found)
    """
    league_bounding_box = get_window_bounding_box(CONSTANTS["window_titles"]["game"])
    if not league_bounding_box:
        return 0

    width = league_bounding_box.get_width()
    height = league_bounding_box.get_height()
    min_x = league_bounding_box.min_x
    min_y = league_bounding_box.min_y

    resize_x = width / 1920
    resize_y = height / 1080

    region = (
        int(min_x + (1650 * resize_x)),
        int(min_y + (150 * resize_y)),
        int(min_x + (1920 * resize_x)),
        int(min_y + (400 * resize_y)),
    )

    checked_champs = []
    for trait in wanted_traits:
        for champion in CONSTANTS["game"]["champions"]["trait"][trait]:
            path = CONSTANTS["game"]["champions"]["full"][champion]
            if champion not in checked_champs:
                if get_on_screen_in_game(path=path, precision=0.95, offsets=region) is not None:
                    return champion
            checked_champs.append(champion)

    return None