"""
Module holding the OCR standard economy mode.
"""
from loguru import logger
from pytesseract import pytesseract

from tft import GAME_CLIENT_INTEGRATION

from ..helpers import screen_helpers
from .base import EconomyMode

class OCRStandardEconomyMode(EconomyMode):
    """
    OCR standard economy mode implementation.
    """

    def __init__(self, wanted_traits: list[str], prioritized_order: bool, tesseract_location: str): 
        super().__init__(wanted_traits, prioritized_order, tesseract_location)
        pytesseract.tesseract_cmd = tesseract_location

    def loop_decision(self, current_round: int, event: int):
        if event != 0:
            if event == 1:
                self.bench_cleanup()
                logger.debug("Triggered event bench_cleanup")
            elif event == 2:
                self.board_cleanup(current_round=current_round)
                logger.debug("Triggered event board_cleanup")
            elif event == 3:
                self.collect_items()
                logger.debug("Triggered event collect_items")
            elif event == 4:
                self.place_items()
                logger.debug("Triggered event place_items")
            return

        self.walk_random()
        self.purchase_units(amount=3)

        # just buy champs till then. no other spendings
        if current_round <= 30:
            return

        gold = screen_helpers.get_gold_with_ocr()
        logger.debug(f"OCR recognized {gold} gold")

        while (gold >= 58 or current_round >= 60 and gold >= 24) and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            gold -= 4

        if gold >= 55 or (current_round >= 60 and gold >= 35):
            self.roll()