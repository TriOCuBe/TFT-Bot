"""A collection of system-level helpers"""
import os
import pathlib
import re
import socket
import winreg

from loguru import logger
import psutil
import win32com.client
import win32gui
import win32process

from tft_bot import config

try:
    import ctypes
    import msvcrt
except Exception:
    pass


def set_active_window(window_id: int) -> None:
    """Sets the currently active window and focus.

    Args:
        window_id (int): The window ID to use
    """
    # Try to account for every scenario
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("%")
    win32gui.BringWindowToTop(window_id)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)


def bring_window_to_forefront(window_title: str, path_to_verify: str | None = None) -> None:
    """Bring the first window found matching the requested title to the forefront and focus/make active.

    Args:
        window_title (str): The window title to match/look for.
        path_to_verify (str | None, optional): If provided, validates the window found matching the title is this
            executable path. Defaults to None.
    """
    try:
        hwnd = win32gui.FindWindowEx(0, 0, 0, window_title)
        if path_to_verify is not None:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            path = psutil.Process(pid).exe()
            if path != path_to_verify:
                logger.debug(f"Failed to find process to bring to forefront:\n\t{path} != {path_to_verify}")
                return
        set_active_window(hwnd)
    except Exception as err:
        logger.debug(f"Failed to click to {err}")


def find_in_processes(executable_path: str) -> bool:
    """Find if the provided executable path is one of the currently active processes.

    Args:
        executable_path (str): The executable path to check for.

    Returns:
        bool: True if the requested executable path was found, False otherwise.
    """
    for proc in psutil.process_iter():
        try:
            if proc.exe() == executable_path:
                return True
        except Exception:
            # Nothing, we don't care
            continue
    return False


def internet(host="1.1.1.1", port=53) -> bool:
    """
    Checks if there is an active internet connection to the given IP address.

    Args:
        host: The host to connect to. Defaults to "1.1.1.1".
        port: The port to connect on. Defaults to 53 (TCP/UDP port for DNS service)

    Returns:
        bool: True if the connection succeeds to the specified IP address, False otherwise.
    """
    try:
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False


# Via https://gist.github.com/sthonnard/31106e47eab8d6f3329ef530717e8079
def disable_quickedit() -> None:
    """Disable QuickEdit mode on Windows terminal. QuickEdit pauses application execution if the user
    selects/highlights/clicks within the terminal.
    """
    if not os.name == "posix":
        try:
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            device = r"\\.\CONIN$"
            with open(device, "r") as con:  # pylint: disable=unspecified-encoding
                file_handle = msvcrt.get_osfhandle(con.fileno())
                kernel32.SetConsoleMode(file_handle, 0x0081)
        except Exception as err:
            logger.warning(f"Cannot disable QuickEdit mode! : {str(err)}")
            logger.warning("As a consequence, execution might be automatically paused, careful where you click!")


def expand_environment_variables(var: str) -> str:
    """Expands the provided variable for any included environment variables.

    Args:
        var (str): The string containing environment variables.

    Returns:
        str: The string with any environment variables replaced.
    """
    return os.path.expandvars(var)


def read_registry(hkey_type: int, path: str, value: str) -> str | None:
    """
    Read the registry at a specific hkey type and path.

    Args:
        hkey_type: The HKEY to read at, see winreg.HKEY_*
        path: The path to read at.
        value: The specific value to read from the path

    Returns:
        The value as a str if found, otherwise None.
    """
    try:
        access_registry = winreg.ConnectRegistry(None, hkey_type)
        access_key = winreg.OpenKey(
            access_registry,
            path,
            0,
            winreg.KEY_READ,
        )
        [path, _] = winreg.QueryValueEx(access_key, value)
    except Exception as exc:
        logger.opt(exception=exc).error(f"Could not read registry at {path}\\{value}.")
        return None

    return path


def determine_league_install_location() -> str:
    """Determine the location League was installed.

    Returns:
        str: If successful, the determined install location. If unsuccessful, the default install location.
    """
    # Assign default just in case it failed to be found
    league_path = r"C:\Riot Games\League of Legends"
    override_path = config.get_override_install_location("league_client")

    if override_path is not None:
        logger.warning(f"Override path supplied, using '{override_path}' as League install directory.")
        league_path = override_path
    else:
        registry_entry = read_registry(
            hkey_type=winreg.HKEY_CURRENT_USER,
            path=r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Riot Game league_of_legends.live",
            value="InstallLocation",
        )
        if registry_entry:
            league_path = registry_entry

    league_path = str(pathlib.PureWindowsPath(league_path))

    logger.debug(f"League path determined to be: {league_path}")

    return league_path


def determine_riot_client_install_location() -> str:
    """Determine the location League was installed.

    Returns:
        str: If successful, the determined install location. If unsuccessful, the default install location.
    """
    # Assign default just in case it failed to be found
    riot_path = r"C:\Riot Games\Riot Client"
    override_path = config.get_override_install_location("riot_client")

    if override_path is not None:
        logger.warning(f"Override path supplied, using '{override_path}' as League install directory.")
        riot_path = override_path
    else:
        registry_entry = read_registry(
            hkey_type=winreg.HKEY_CURRENT_USER,
            path=r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Riot Game league_of_legends.live",
            value="UninstallString",
        )
        # The only way we can parse the install location of client services is from the league uninstallation
        # registry entry, so we parse it to ensure we strip the uninstall args
        if registry_entry and r"Riot Client\RiotClientServices.exe" in registry_entry:
            try:
                search_result = re.search(r".*Riot Client\\RiotClientServices.exe", registry_entry)
                riot_path = search_result.group()[1:]
                riot_path = re.search(r".*\\Riot Client", riot_path).group()
            except Exception:
                pass

    riot_path = str(pathlib.PureWindowsPath(riot_path))

    logger.debug(f"Riot client path determined to be: {riot_path}")

    return riot_path


def determine_tesseract_ocr_install_location() -> str:
    """
    Determine the location Tesseract-OCR was installed at.

    Returns:
        If successful, the determined install location. If unsuccessful, the default install location.
    """
    tesseract_ocr_path = r"C:\Program Files\Tesseract-OCR"
    override_path = config.get_tesseract_override_install_location()

    if override_path is not None:
        logger.warning(f"Override path supplied, using '{override_path}' as Tesseract-OCR install directory.")
        tesseract_ocr_path = override_path
    else:
        registry_entry = read_registry(
            hkey_type=winreg.HKEY_LOCAL_MACHINE, path=r"SOFTWARE\Tesseract-OCR", value="InstallDir"
        )
        if registry_entry:
            tesseract_ocr_path = registry_entry

        tesseract_ocr_path = str(pathlib.PureWindowsPath(tesseract_ocr_path))

    logger.debug(f"Tesseract-OCR location determined to be: {tesseract_ocr_path}")

    return tesseract_ocr_path

def determine_deceive_install_location() -> str | None:
    """
    Tries to determine the install location of Deceive.

    Returns:
    If successful, a string of the determined location, if not, None.
    """
    # Check downloads folder first. Might just find it
    downloads_path = str(pathlib.Path.home() / "Downloads")
    for root, dirs, files in os.walk(downloads_path):
        for file in files:
            if "Deceive" in file:
                logger.debug("Found Deceive in Downloads folder")
                return os.path.join(root, file)
    
    # Search registry now
    key_to_read = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store"
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_to_read, 0, winreg.KEY_READ)

    for i in range(0, winreg.QueryInfoKey(k)[1]):
        if "Deceive" in winreg.EnumValue(k, i)[0]:
            logger.Debug("Found Deceive through registry")
            return winreg.EnumValue(k, i)[0]

    return None