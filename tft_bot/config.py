"""
Module to handle the configuration for the bot.
"""
import argparse
from enum import auto
from enum import StrEnum
import os.path
import shutil
from typing import Any

from loguru import logger
from ruamel.yaml import YAML

from .economy.base import EconomyMode
from .economy.default import DefaultEconomyMode
from .economy.ocr_standard import OCRStandardEconomyMode

_SELF: dict[str, Any] = {}


class Timeout(StrEnum):
    """
    ENUM class to hold the various names of timeouts we allow to be configured.
    """

    UPDATE_NOTIFIER = auto()
    LEAGUE_CLIENT = auto()
    CLIENT_CONNECT = auto()
    CLIENT_AVAILABILITY = auto()
    GAME_WINDOW = auto()
    GAME_START = auto()
    EXIT_BUTTON = auto()
    GRACEFUL_EXIT = auto()
    SURRENDER_MIN = auto()
    SURRENDER_MAX = auto()


def load_config(storage_path: str) -> None:
    """
    Writes the configuration from resource (provided in repository) to storage path, loads the configuration from
    storage path to memory and updates the configuration if necessary.

    Args:
        storage_path: The base storage path where all of our files should go.

    """
    yaml = YAML()

    config_resource_path = "tft_bot/resources/config.yaml"
    config_path = f"{storage_path}\\config.yaml"

    # Create output directory if it does not exist
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    if not os.path.isfile(config_path):
        shutil.copyfile(config_resource_path, config_path)

    with open(config_resource_path, mode="r", encoding="UTF-8") as config_resource:
        _config_resource: dict[str, Any] = yaml.load(config_resource)

    with open(config_path, mode="r", encoding="UTF-8") as config_file:
        global _SELF
        _SELF = yaml.load(config_file)

    if _config_resource.get("version") > _SELF.get("version", 0):
        logger.warning("Config is outdated, creating a back-up and updating it")

        shutil.copyfile(config_path, f"{config_path}.bak")

        if _config_resource.get("set") > _SELF.get("set", 8.5):
            logger.warning("There is a new set, updating wanted_traits as well")
            _SELF["wanted_traits"] = _config_resource["wanted_traits"]

        _config_resource.update((key, _SELF[key]) for key in _SELF.keys() & _config_resource.keys() if key != "version")
        with open(config_path, mode="w", encoding="UTF-8") as config_file:
            yaml.dump(_config_resource, config_file)

        _SELF = _config_resource

    _parse_cli_flags()


def _parse_cli_flags() -> None:
    """
    Override settings for the bot with CLI flags, since they take higher precedence.
    """
    arg_parser = argparse.ArgumentParser(prog="TFT Bot")
    arg_parser.add_argument(
        "-f",
        "--ffearly",
        action="store_true",
        help="If the game should be surrendered at first available time.",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase output verbosity, mostly useful for debugging",
    )
    parsed_args = arg_parser.parse_args()

    if parsed_args.ffearly:
        _SELF["forfeit_early"] = True

    if parsed_args.verbose:
        _SELF["log_level"] = "DEBUG"


def get_log_level() -> str:
    """
    Get the level we're supposed to log at from the config.

    Returns:
        The configured level as a str.

    """
    return _SELF.get("log_level", "INFO")


def forfeit_early() -> bool:
    """
    Get the state of the forfeit_early setting in the config.

    Returns:
        True if we should surrender early, False if not.

    """
    return _SELF.get("forfeit_early", False)


def get_override_install_location(app: str) -> str | None:
    """
    Get the value of the override_install_location setting in the config.

    Returns:
        An optional string containing the user-defined install location.

    """
    return _SELF.get(f"override_install_location_{app}") or None


def get_wanted_traits() -> list[str]:
    """
    Get the list of traits we attempt to purchase.

    Returns:
        A list of traits we look for.

    """
    return _SELF.get("wanted_traits", ["duelist", "brawler"])


def purchase_traits_in_prioritized_order() -> bool:
    """
    Get if we should purchase traits in prioritized order.

    Returns:
        True if we should only buy a trait if the trait before it has been found, False if not.

    """
    return _SELF.get("purchase_traits_in_prioritized_order", True)


def get_timeout(timeout: Timeout, default: int) -> int:
    """
    Get a timeout value by enum class member.

    Args:
        timeout: The timeout to get from the config.
        default: The default to fall back to, if the value is missing in the config.

    Returns:
        The timeout in seconds.

    """
    return _SELF.get(timeout, default)


def get_tesseract_override_install_location() -> str | None:
    """
    Get the value of the override_tesseract_location setting in the config.

    Returns:
        An optional string containing the user-defined install location.

    """
    return _SELF["economy"].get("override_tesseract_location") or None


def get_economy_mode(system_helpers) -> EconomyMode:
    """
    Get the economy mode the bot should run on.

    Args:
        system_helpers: Dependency injected system_helpers module.

    Returns:
        A new instance of the economy mode.

    """
    wanted_traits = get_wanted_traits()
    prioritized_order = purchase_traits_in_prioritized_order()

    match _SELF["economy"].get("mode", "default"):
        case "default":
            return DefaultEconomyMode(wanted_traits=wanted_traits, prioritized_order=prioritized_order)
        case "ocr_standard":
            tesseract_location = system_helpers.determine_tesseract_ocr_install_location() + "\\tesseract.exe"
            if not os.path.isfile(tesseract_location):
                logger.warning(
                    f'Tesseract location "{tesseract_location}" does not exist. Falling back to default economy mode'
                )
                return DefaultEconomyMode(wanted_traits=wanted_traits, prioritized_order=prioritized_order)

            return OCRStandardEconomyMode(
                wanted_traits=wanted_traits, prioritized_order=prioritized_order, tesseract_location=tesseract_location
            )


def get_tesseract_location(system_helpers) -> str | None:
    """
    Get location of tesseract

    Args:
        system_helpers: Dependency injected system_helpers module.

    Returns:
        String or None
    """
    tesseract_location: str = system_helpers.determine_tesseract_ocr_install_location() + "\\tesseract.exe"
    if not os.path.isfile(tesseract_location):
        return None

    return tesseract_location


def get_item_config() -> bool:
    """
    Get the config for items.

    Returns:
        True or False for on or off
    """
    return _SELF.get("items", False)


def get_round_ocr_config() -> bool:
    """
    Get the config for get_round method.

    Returns:
        True or False for OCR or cv2.
    """
    return _SELF.get("ocr_for_rounds", False)


def get_deceive_config() -> bool:
    """
    Checks if the bot should use Deceive.

    Returns:
        True or False.
    """
    return _SELF.get("use_deceive", False)


def get_install_location_deceive() -> str | None:
    """
    Gets the path of Deceive.exe.

    Returns:
        String containing path or None if empty.
    """
    return _SELF.get("install_location_deceive") or None


def update_deceive_config(update: bool) -> None:
    """
    Updates whether the bot should use Deceive or not.

    Args:
        update: The new bool that should be used henceforth
    """
    _SELF["use_deceive"] = update
