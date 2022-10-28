import time
import python_imagesearch.imagesearch as imagesearch

def onscreen(path, precision=0.8):
    return imagesearch.imagesearch(path, precision)[0] != -1

def onscreen_multiple_any(paths, precision=0.8):
    for path in paths:
        if (imagesearch.imagesearch(path, precision)[0] != -1):
            return True
    return False

def onscreen_region(path, x1, y1, x2, y2, precision=0.8):
    return imagesearch.imagesearcharea(path, x1, y1, x2, y2, precision)[0] != -1

def onscreen_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision=0.8):
    return imagesearch_region_numLoop(path, timesample, maxSamples, x1, y1, x2, y2, precision)[0] != -1

# Via https://github.com/drov0/python-imagesearch/blob/master/python_imagesearch/imagesearch.py
def imagesearch_region_numLoop(image, timesample, maxSamples, x1, y1, x2, y2, precision=0.8):
    pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
    count = 0

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearch.imagesearcharea(image, x1, y1, x2, y2, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos