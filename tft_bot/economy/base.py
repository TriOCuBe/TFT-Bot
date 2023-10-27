"""
Module holding the base economy mode blueprint class.
"""
import time
import random

from tft_bot.constants import CONSTANTS
from tft_bot.helpers.click_helpers import click_to, click_to_image, move_to, hold_and_move_to, press
from tft_bot.helpers.screen_helpers import get_on_screen_in_game, calculate_window_click_offset


class EconomyMode:
    """
    Blueprint class to implement custom economy modes on.
    """

    def __init__(self, wanted_traits: list[str], prioritized_order: bool):
        """
        Init method to dependency-inject the purchase logic.
        Args:
            wanted_traits: A list of wanted traits.
            prioritized_order: Whether to only buy a trait if the trait before it was bought.
        """
        self.wanted_traits = wanted_traits
        self.prioritized_order = prioritized_order

    def loop_decision(self, minimum_round: int) -> None:
        """
        Method to be called by the main game loop for the mode to make a decision.

        Args:
            minimum_round: The n-th round (N-*) we are at.
        """
        raise NotImplementedError

    def purchase_units(self, amount: int) -> None:
        """
        Attempts to purchase a given amount of units from the pool of configured traits.

        Args:
            amount: The amount of units to purchase.
        """
        for _ in range(amount):
            for trait in self.wanted_traits:
                if click_to_image(image_search_result=get_on_screen_in_game(CONSTANTS["game"]["trait"][trait])):
                    time.sleep(0.5)
                elif self.prioritized_order:
                    return

    def sell_units(self, amount: int) -> None:
        # y=780, x=400 + 130 * 8 (total 9)
        """
        Attempts to sell a random unit on the bench.

        Args:
            amount: The amount of units to sell.
        """

        points = []
        for i in range(9):
            point = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=410 + (120 * i), position_y=780)
            points.append({"x": point.position_x, "y": point.position_y})

        for _ in range(amount):
            # this block removes used points, so the same slot can't be picked multiple times
            index = random.randint(0, len(points)-1)
            point = points[index]
            points.remove(point)

            move_to(position_x=point["x"], position_y=point["y"])
            if random.randint(0, 1) == 1:
                sell_offset = calculate_window_click_offset(
                    window_title=CONSTANTS["window_titles"]["game"], position_x=random.randint(850, 1000), position_y=980
                )
                hold_and_move_to(sell_offset.position_x, sell_offset.position_y)
            else:
                press('E')  # hotkey for sell

    def roll(self) -> None:
        """
        Utility method to roll (refresh) the shop once.
        """
        if random.randint(0, 1) == 1:
            click_to_image(image_search_result=get_on_screen_in_game(CONSTANTS["game"]["gamelogic"]["reroll"]))
        else:
            press('D')  # hotkey for roll

    def purchase_xp(self) -> None:
        """
        Utility method to purchase xp once.
        """
        if random.randint(0, 1) == 1:
            click_to_image(image_search_result=get_on_screen_in_game(CONSTANTS["game"]["gamelogic"]["xp_buy"]))
        else:
            press('F')  # hotkey for xp

    # unused
    # def collect_items(self) -> None:
    #     """
    #     Runs a circle (square) around the map, trying to collect items on the way.
    #     """
    #     checkpoint1 = calculate_window_click_offset(
    #         window_title=CONSTANTS["window_titles"]["game"], position_x=500, position_y=650
    #     )
    #     checkpoint2 = calculate_window_click_offset(
    #         window_title=CONSTANTS["window_titles"]["game"], position_x=1400, position_y=650
    #     )
    #     checkpoint3 = calculate_window_click_offset(
    #         window_title=CONSTANTS["window_titles"]["game"], position_x=1400, position_y=300
    #     )
    #     checkpoint4 = calculate_window_click_offset(
    #         window_title=CONSTANTS["window_titles"]["game"], position_x=500, position_y=300
    #     )
    #     logger.info("Running around, trying to collect items")

    #     checkpoint_list = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]
    #     # for i in range(2):
    #     random.shuffle(checkpoint_list)
    #     for point in checkpoint_list:
    #         click_to(position_x=point.x, position_y=point.y, action="right")
    #         time.sleep(2.5)

    def walk_random(self) -> None:
        """
        Walks to a random point on the field.
        """
        goal_offset = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], 
            position_x=random.randint(500, 1200), 
            position_y=random.randint(300, 650)
        )

        click_to(position_x=goal_offset.position_x, position_y=goal_offset.position_y, action="right")