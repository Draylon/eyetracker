import os
import pygame as pg
import win32api
import win32con
import win32gui

SCREEN_SIZE = (1920,1080)

os.environ['SDL_VIDEO_CENTERED'] = '1'

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE, pg.SCALED | pg.FULLSCREEN)
done = False
fuchsia = (255, 0, 128)
dark_red = (139, 0, 0)

hwnd = pg.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    screen.fill(fuchsia)
    #pg.draw.rect(screen,)
    pg.draw.rect(screen, dark_red, pg.Rect(30, 30, 60, 60))
    pg.display.update()