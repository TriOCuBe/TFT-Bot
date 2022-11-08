import time
import python_imagesearch.imagesearch as imagesearch
import logging

def onscreen(path, precision=0.8) -> bool:
    try:
        return imagesearch.imagesearch(path, precision)[0] != -1
    except Exception:
        return False

def onscreen_multiple_any(paths, precision=0.8) -> bool:
    try:
        for path in paths:
            is_onscreen = imagesearch.imagesearch(path, precision)[0]
            # logging.debug(f"is_onscreen: {is_onscreen != -1}") #Advanced debugging not even normally needed
            if (is_onscreen != -1):
                return True
    except Exception as err:
        logging.debug(f"multiple_onscreen_any error: {err}")

    return False

def onscreen_region(path, x1, y1, x2, y2, precision=0.8) -> (bool | list[int] | tuple[int, int]):
    try:
        pos = imagesearch.imagesearcharea(path, x1, y1, x2, y2, precision)
        return pos if pos[0] != -1 else False
    except Exception:
        return False

def onscreen_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision=0.8) -> (bool | list[int] | tuple[int, int]):
    try:
        return imagesearch_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision)[0] != -1
    except Exception:
        return False

# Via https://github.com/drov0/python-imagesearch/blob/master/python_imagesearch/imagesearch.py
def imagesearch_region_numLoop(image, timesample, maxSamples, x1, y1, x2, y2, precision=0.8) -> (None | list[int] | tuple[int, int]):
    try:
        pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
        count = 0

        while pos[0] == -1:
            time.sleep(timesample)
            pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
            count = count + 1
            if count > maxSamples:
                break
        return pos
    except Exception:
        return None

def find_image(path, precision=0.8) -> (None | list[int] | tuple[int, int]):
    try:
        pos = imagesearch.imagesearch(path, precision)
        return pos if pos[0] != -1 else None
    except Exception:
        return None

def find_image_multiple_any(paths, precision=0.8) -> (None | list[int] | tuple[int, int]):
    try:
        for path in paths:
            pos = imagesearch.imagesearch(path, precision)
            # logging.debug(f"is_onscreen: {pos[0] != -1}") #Advanced debugging not even normally needed
            if (pos[0] != -1):
                return pos
            else:
                return None
    except Exception as err:
        logging.debug(f"multiple_onscreen_any error: {err}")

    return None

def find_image_in_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision=0.8) -> (None | list[int] | tuple[int, int]):
    try:
        pos = imagesearch_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision)
        return pos if pos[0] != -1 else None
    except Exception:
        return None