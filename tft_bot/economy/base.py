"""
Module holding the base economy mode blueprint class.
"""
from time import sleep
import random
import keyboard
from loguru import logger

from tft_bot.constants import CONSTANTS
from tft_bot.helpers.click_helpers import click_to, click_to_image, move_to, hold_and_move_to, press
from tft_bot.helpers.screen_helpers import get_on_screen_in_game, calculate_window_click_offset, get_items, check_champion


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
        self.items: list = []
        self.bench_targets: list[tuple][int, int] = CONSTANTS["game"]["coordinates"]["bench"][:]

    def loop_decision(self, minimum_round: int, event: int) -> None:
        """
        Method to be called by the main game loop for the mode to make a decision.

        Args:
        minimum_round: The n-th round (N-*) we are at.
        event: What event to trigger. No event if event == 0
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
                    sleep(0.5)
                elif self.prioritized_order:
                    return

    def sell_unit(self, coordinates: tuple[int, int], calculate_offset: bool = True) -> None:
        """
        Attempts to sell a unit.

        Args:
        coordinates: Coordinates of the champion to sell in a tuple
        calculate_offset: Wether to calculate the offset of the given coordinates or not. Defaults to True
        """
        if calculate_offset:
            point = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=coordinates[0], position_y=coordinates[1])
            coordinates = (point.position_x, point.position_y)

        move_to(position_x=coordinates[0], position_y=coordinates[1])
        sleep(0.5)

        if random.randint(0, 1) == 1:
            sell_offset = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=random.randint(800, 1300), position_y=980)
            hold_and_move_to(sell_offset.position_x, sell_offset.position_y)
        else:
            press('E')

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

    def collect_items(self) -> None:
        """
        Runs a circle (square) around the map, trying to collect items on the way.
        """
        checkpoint1 = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=550, position_y=620
        )
        checkpoint2 = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=1300, position_y=650
        )
        checkpoint3 = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=1250, position_y=250
        )
        checkpoint4 = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=600, position_y=250
        )
        checkpoint_list = [checkpoint1, checkpoint2, checkpoint3, checkpoint4]
        random.shuffle(checkpoint_list)
        for point in checkpoint_list:
            click_to(position_x=point.position_x, position_y=point.position_y, action="right")
            sleep(2.5)

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

    # essentially copied from https://github.com/jfd02/TFT-OCR-BOT/blob/main/arena.py#L203
    def place_items(self) -> None:
        """
        Places items on bench on random champs
        """
        self.items = get_items()
        for index, _ in enumerate(self.items):
            if self.items[index] is not None:
                self.add_item_to_champ(index)

    # cont
    def add_item_to_champ(self, item_index: int) -> None:
        """
        Take given item and add it to random champ on board.

        Args:
            item_index: The index of the item, in order to determine its position
        """
        item = self.items[item_index]
        targets = self.get_board_targets()[2:]
        target_champion = random.choice(targets)

        # don't need to calculate offset as the coordinates in the list were already run through that in get_items()
        move_to(item[0], item[1])
        sleep(0.5)

        champion_offset = calculate_window_click_offset(
            window_title=CONSTANTS["window_titles"]["game"], position_x=target_champion[0], position_y=target_champion[1]
        )
        hold_and_move_to(champion_offset.position_x, champion_offset.position_y)
        sleep(0.5)

    def get_board_targets(self) -> list:
        """
        Checks current level and how many champions we expect there to be on the board.

        Returns:
        List of coordinates of board champions. Length is equal to current level/expected amount of champs.
        """
        from tft import GAME_CLIENT_INTEGRATION

        level = GAME_CLIENT_INTEGRATION.get_level()
        board_targets = CONSTANTS["game"]["coordinates"]["board"][:level + 2]

        return board_targets

    def check_bench(self) -> None:
        """
        Checks what champions are currently on the bench.

        Returns:
        List of str or None.
        """
        bench_champions = []
        # safe_point = calculate_window_click_offset(CONSTANTS["window_titles"]["game"], position_x=800, position_y=625)
        for coordinates in self.bench_targets:
            point = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=coordinates[0], position_y=coordinates[1]-25)

            click_to(position_x=point.position_x, position_y=point.position_y, action="right")

            champion = check_champion(self.wanted_traits)
            bench_champions.append(champion)

        return bench_champions

    def check_board(self) -> None:
        """
        Checks what champions are currently on the board.

        Returns:
        List of str or None. Length of list is equal to number of expected champions.
        """
        board_champions = []
        board_targets = self.get_board_targets()
        for coordinates in board_targets:
            point = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=coordinates[0], position_y=coordinates[1])

            click_to(position_x=point.position_x, position_y=point.position_y, action="right")

            champion = check_champion(self.wanted_traits)
            board_champions.append(champion)

        return board_champions

    def bench_cleanup(self) -> None:
        """
        Sells all champions we don't want on the bench.
        """
        bench_champions = self.check_bench()
        index = 0
        for champion in bench_champions:
            if champion is None:
                target = self.bench_targets[index]
                self.sell_unit(target)
                sleep(0.5)
            index += 1

    def board_cleanup(self, current_round: int) -> None:
        """
        Sells all champions we don't want on the board.
        """
        ocr_round = False
        # if we are using ocr, we get rounds as double digits (12, 34, 55 etc). That means if the int is > 8, we are using ocr
        if current_round > 8:
            ocr_round = True

        board_champions = self.check_board()
        board_targets = self.get_board_targets()
        
        known_champions = []
        index = 0
        for champion in board_champions:
            if champion is None:
                target = board_targets[index]
                self.sell_unit(target)
                sleep(0.1)

            # this sells duplicate champs, even if they have the trait we want. Only triggers round 4 onwards
            elif ((ocr_round and current_round > 40) or (not ocr_round and current_round > 3)) and champion in known_champions:
                target = board_targets[index]
                self.sell_unit(target)
                sleep(0.1)
            
            known_champions.append(champion)
            index += 1