"""
Module holding the default economy mode.
"""
import time
import random

from tft import GAME_CLIENT_INTEGRATION

from ..helpers import screen_helpers
from .base import EconomyMode


class DefaultEconomyMode(EconomyMode):
    """
    Default economy mode implementation.
    """

    def loop_decision(self, minimum_round: int):
        if screen_helpers.gold_at_least(3):
            self.purchase_units(amount=3)
            time.sleep(0.5)

        if minimum_round < 3:
            return

        if screen_helpers.gold_at_least(4) and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            time.sleep(0.5)

        if screen_helpers.gold_at_least(5):
            self.roll()
            time.sleep(0.5)

        if random.randint(0, 2) == 1:
            self.sell_units(amount=random.randint(1,2))
            time.sleep(0.5)
    
        global timer
        if timer is undefined:
            timer = 0

        if timer >= 10:
            self.collect_items()
        else:
            timer += 1
        time.sleep(0.5)