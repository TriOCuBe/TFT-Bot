import win32gui
import win32process
import win32com.client

import logging
import psutil

def set_active_window(window_id):
    # Try to account for every scenario
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.BringWindowToTop(window_id)
    win32gui.SetForegroundWindow(window_id)
    win32gui.SetActiveWindow(window_id)

def bring_window_to_forefront(window_title, path_to_verify=None):
    try:
        hwnd = win32gui.FindWindowEx(0,0,0, window_title)
        if (path_to_verify is not None):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            path = psutil.Process(pid).exe()
            if path != path_to_verify:
                logging.debug(f"Failed to find process to bring to forefront:\n\t{path} != {path_to_verify}")
                return
        set_active_window(hwnd)
    except Exception as err:
        logging.debug(f"Failed to click to {err}")

def find_in_processes(executable_path):
    for proc in psutil.process_iter():
        try:
            if (proc.exe() == executable_path):
                return True
        except Exception:
            # Nothing, we don't care
            continue
    return False
