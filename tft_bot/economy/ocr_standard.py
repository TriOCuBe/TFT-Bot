"""
Module holding the OCR standard economy mode.
"""
from loguru import logger
from pytesseract import pytesseract
from time import sleep

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

    def loop_decision(self, minimum_round: int, event: bool):
        self.walk_random()
        sleep(0.5)

        self.purchase_units(amount=3)
        sleep(0.5)

        self.place_items()
        sleep(0.5)
        # just buy champs till then. no other spendings
        if minimum_round <= 2:
            return

        gold = screen_helpers.get_gold_with_ocr()
        logger.debug(f"OCR recognized {gold} gold")

        if gold >= 54 and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            gold -= 4
            if gold >= 54:
                self.purchase_xp()
                gold -= 4

        if minimum_round <= 3:
            return

        # if minimum_round == 1 or (gold >= 5 and minimum_round == 2):
        #     self.purchase_units(amount=3)
        #     time.sleep(0.5)
        #     return
        # elif gold >= 35 and minimum_round <= 3:
        #     self.purchase_units(amount=3)
        #     if random.randint(0, 3) == 1:
        #         self.sell_units(amount=2)
        #     return
        # elif gold >= 55:
        #     self.purchase_units(amount=3)

        if event:
            event = False
            logger.debug("Triggering event, selling a bunch of champs")

            self.sell_units(amount=5)
            sleep(0.5)

            self.roll()
            sleep(0.5)
            self.purchase_units(3)
            sleep(0.5)
            
            for _ in range(3):
                self.walk_random()
                sleep(1.5)

        gold = screen_helpers.get_gold_with_ocr()
        logger.debug(f"OCR recognized {gold} gold buying and selling")

        if gold >= 58:
            self.roll()

        return event