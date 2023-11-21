from tft import restart_league_client
from tft_bot import config
import time

config.load_config()
while True:
    restart_league_client()
    time.sleep(5)