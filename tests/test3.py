import threading
import pygame as pg


class Game ():
    
    engine_running = True
    gui_running = True
    clock = pg.time.Clock()

    gui_framerate = 60.0
    engine_framerate = 120.0

    def __init__(self,draw_function):

        pg.init()
        pg.display.set_caption('Explodotech')
        self.window_surface = pg.display.set_mode((800, 600))
        self.background = pg.Surface((800, 600))
        self.background.fill(pg.Color('#000000'))

        self._draw_function = draw_function
        
        ### Create and start the threads
        self.mainthread = threading.Thread(target = self.mainloop)
        self.mainthread.start()
        
    def __del__(self):
        self.stop_view()
        
    def start_view(self):
        """Starts the main loop"""
        self.mainthread_running = True

    def stop_view(self):
        """Stops the main loop"""
        self.mainthread_running = False

    def mainloop(self):
        """Managing all the GUI stuff"""

        while self.mainthread_running:
            self._draw_function()