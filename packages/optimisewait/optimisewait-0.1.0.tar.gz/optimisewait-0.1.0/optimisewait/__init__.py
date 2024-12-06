import pyautogui
from time import sleep

_default_autopath = r'C:\\'

def set_autopath(path):
    global _default_autopath
    _default_autopath = path

def optimiseWait(filename, dontwait=False, specreg=None, clicks=1, xoff=0, yoff=0, autopath=None):
    global _default_autopath
    autopath = autopath if autopath is not None else _default_autopath

    if not isinstance(filename, list):
        filename = [filename]
    if not isinstance(clicks, list):
        clicks = [clicks] + [1] * (len(filename) - 1)
    elif len(clicks) < len(filename):
        clicks = clicks + [1] * (len(filename) - len(clicks))

    clicked = 0
    while True:
        findloc = None
        for i, fname in enumerate(filename):
            try:
                if specreg is None:
                    loc = pyautogui.locateCenterOnScreen(fr'{autopath}\{fname}.png', confidence=0.9)
                    if loc and clicked == 0:
                        findloc = loc
                        clicked = i + 1
                else:
                    loc = pyautogui.locateOnScreen(fr'{autopath}\{fname}.png', region=specreg, confidence=0.9)
                    if loc:
                        findloc = loc
                        clicked = i + 1
            except pyautogui.ImageNotFoundException:
                continue

        if dontwait is False:
            if findloc:
                break
        else:
            if not findloc:
                return {'found': False, 'image': None}
            else:
                return {'found': True, 'image': filename[clicked - 1]}
        sleep(1)

    if findloc is not None:
        if specreg is None:
            x, y = findloc
        else:
            x, y, width, height = findloc
        xmod = x + xoff
        ymod = y + yoff
        sleep(1)

        click_count = clicks[clicked - 1] if clicked > 0 else 0
        if click_count > 0:
            for _ in range(click_count):
                pyautogui.click(xmod, ymod)
                sleep(0.1)
        
        return {'found': True, 'image': filename[clicked - 1]}
    
    return {'found': False, 'image': None}
