from tft_bot.helpers.screen_helpers import calculate_window_click_offset
from tft_bot.helpers.click_helpers import hold_and_move_to, move_to
from tft_bot.constants import CONSTANTS
import random
import time

time.sleep(4)
points = []
for i in range(9):
    # point = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=400 + (130 * i), position_y=780)
    point = {"position_x": (410 + (120 * i)) * (10/12), "position_y": 780 * (10/12)}
    points.append(point)

for _ in range(9):
    # this block removes used points, so the same slot can't be picked multiple times
    index = random.randint(0, len(points)-1)
    point = points[index]
    points.remove(point)

    move_to(position_x=point["position_x"], position_y=point["position_y"])
    # sell_offset = calculate_window_click_offset(window_title=CONSTANTS["window_titles"]["game"], position_x=960, position_y=980)
    sell_offset = {"position_x": 960 * (10/12), "position_y": 980 * (10/12)}
    hold_and_move_to(sell_offset["position_x"], sell_offset["position_y"])