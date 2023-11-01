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

    def loop_decision(self, current_round: int, event: bool, item_config: bool):
        if event:
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
        time.sleep(0.5)

        if screen_helpers.gold_at_least(3):
            self.purchase_units(amount=3)
            time.sleep(0.5)

        if random.randint(0, 8) == 1 and get_item_config():    
            self.place_items()
            sleep(0.5)

        if current_round[1] < 2:
            return

        if screen_helpers.gold_at_least(4) and GAME_CLIENT_INTEGRATION.get_level() < 8:
            self.purchase_xp()
            time.sleep(0.5)
            if current_round[1] >= 4:
                self.purchase_xp()
                time.sleep(0.5)
            if current_round[1] >= 5:
                self.purchase_xp()
                time.sleep(0.5)

        if random.randint(0, 10) == 1:
            self.board_cleanup
            time.sleep(0.5)

        if current_round[1] < 3:
            return

        if screen_helpers.gold_at_least(5):
            self.roll()
            time.sleep(0.5)
