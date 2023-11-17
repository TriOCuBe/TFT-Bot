from tft_bot import config

config.load_config(storage_path="tft_bot\\output")
print(config.get_log_level())