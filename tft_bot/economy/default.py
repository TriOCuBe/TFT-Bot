"""
Module holding the default economy mode.
"""
import time
import random

from loguru import logger
from tft import GAME_CLIENT_INTEGRATION

from ..helpers import screen_helpers
from .base import EconomyMode


class DefaultEconomyMode(EconomyMode):
    """
    Default economy mode implementation.
    """

    def loop_decision(self, minimum_round: int, event: bool):
        from tft_bot.config import get_item_config

        self.walk_random()
        time.sleep(0.5)

        if screen_helpers.gold_at_least(3):
            self.purchase_units(amount=3)
            time.sleep(0.5)

        if random.randint(0, 8) == 1 and get_item_config():    
            self.place_items()
            sleep(0.5)

        if minimum_round < 2:
            return event

        if screen_helpers.gold_at_least(4) and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            time.sleep(0.5)
            if minimum_round >= 4:
                self.purchase_xp()
                time.sleep(0.5)
            if minimum_round >= 5:
                self.purchase_xp()
                time.sleep(0.5)

        if random.randint(0, 3) == 1:
            self.sell_units(amount=random.randint(1,2))
            time.sleep(0.5)

        if minimum_round < 3:
            return event

        if screen_helpers.gold_at_least(5):
            self.roll()
            time.sleep(0.5)

        if event:
            event = False
            logger.debug("Triggering event, selling a bunch of champs")

            self.sell_units(amount=5)
            sleep(0.5)

            self.roll()
            sleep(0.5)
            self.purchase_units(3)
            sleep(0.5)
            
            self.collect_items()
            self.place_items()
            return event
            
        return event
