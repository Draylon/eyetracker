import pandas as pd
from CamTrack import CamTrack
import pygame as pg
from window import CompWindow

class Training:
    def __init__(self):
        
        self.scr_coords = (0,0)
        
        #create camera object
        #create Window object
        
        self.df_feat = pd.DataFrame()
        self.cam_instance = CamTrack()
        self.cam_instance.set_featureFetch(self.caller)

        #draw/write on window
        self.wnd = CompWindow(self.drawing,self.stageEvents)
        self.wnd.start_worker()


    def drawing(self):
        #draw center
        #animations
        #   directions: center, W, E, N, S, NW, NE, SW, SE
        
        #   directions for: [eye,face]
        pass

    def stageEvents(self,evl):
        #window event
        #get spacebar pressed
        #next stage on drawing
        for event in evl:
            if event.type == pg.QUIT:
                self.wnd.stop_worker()
                #self.done = True
            if event.type == pg.keypress:
                #next_stage

    def caller(self,cam_feats):
        #camera has a new frame to register
        #get the features
        #get the coordinates
        
        print("caller")
        #self.df_feat.append([cam_feats,self.scr_coords])

    def start_worker(self):
        pass

    def stop_worker(self):
        pass