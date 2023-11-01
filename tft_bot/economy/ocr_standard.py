"""
Module holding the OCR standard economy mode.
"""
from loguru import logger
from pytesseract import pytesseract
from time import sleep
import random

from tft import GAME_CLIENT_INTEGRATION

from ..helpers import screen_helpers
from .base import EconomyMode

class OCRStandardEconomyMode(EconomyMode):
    """
    OCR standard economy mode implementation.
    """

    def __init__(self, wanted_traits: list[str], prioritized_order: bool, tesseract_location: str):
        super().__init__(wanted_traits, prioritized_order)
        pytesseract.tesseract_cmd = tesseract_location

    def loop_decision(self, current_round: int, event: bool, item_config: bool):
        if event and random.randint(0, 1) == 1:
            num = random.randint(0, 3 if item_config else 2)
            if num == 0:
                self.bench_cleanup()
            elif num == 1:
                self.board_cleanup()
            elif num == 2:
                self.collect_items()
            else:
                self.place_items()
            return

        self.walk_random()
        self.purchase_units(amount=3)

        # just buy champs till then. no other spendings
        if current_round[1] <= 30:
            return

        gold = screen_helpers.get_gold_with_ocr()
        logger.debug(f"OCR recognized {gold} gold")

        while (gold >= 58 or current_round[1] >= 60 and gold >= 24) and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            gold -= 4

        if gold >= 55 or (current_round[1][0] >= 60 and gold >= 35):
            self.roll()