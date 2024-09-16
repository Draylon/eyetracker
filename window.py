import os
import pygame as pg
import win32api
import win32con
import win32gui

import utils

SCREEN_SIZE = (1920,1080)

os.environ['SDL_VIDEO_CENTERED'] = '1'
fuchsia = (255, 0, 128)
dark_red = (139, 0, 0)

class CompWindow:
    def __init__(self,drawfunc,eventHdl):
        self._drawfunction = drawfunc
        self._eventHandler = eventHdl
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED | pg.FULLSCREEN)
        self._done = False
        
        hwnd = pg.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

    def stop_worker(self):
        self._done=True

    def start_worker(self):
        return self.mainloop()

    def mainloop(self):
        while not self._done:
            self._eventHandler(pg.event.get())
            self.screen.fill(fuchsia)
            #pg.draw.rect(screen,)
            self._drawfunction()
            #pg.draw.rect(screen, dark_red, pg.Rect(30, 30, 60, 60))
            pg.display.update()
            