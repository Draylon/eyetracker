from types import NoneType
from altair import ColorValue
import pandas as pd
from CamTrack import CamTrack
import pygame as pg
from utils import load_training_model
from window import CompWindow
from window import SCREEN_SIZE, dark_red, fuchsia
import cv2 as cv
import numpy as np

class Training:
    def __init__(self,name: str):
        
        self.name = name
        self.scr_coords = (0,0)
        
        #create camera object
        #create Window object
        
        self.df_feat = pd.DataFrame()
        self.cam_instance = CamTrack()
        self.cam_instance.set_featureFetch(self.caller)
        
        #draw/write on window
        self.wnd = CompWindow(self.drawing,self.stageEvents)
        
        #start workers
        print("start workers")
        self.cam_instance.start_worker()
        print("start cam worker")
        
        sc_x = SCREEN_SIZE[0]
        sc_y = SCREEN_SIZE[1]
        self._screen_pos = np.array([
            #  0        1                2             3               4                5              6                 7             8
            (0,0), ( -sc_x/2,0), (-sc_x/2,-sc_y/2),(0,-sc_y/2), (+sc_x/2,-sc_y/2), (+sc_x/2,0), (+sc_x/2,+sc_y/2), (0,+sc_y/2), (-sc_x/2,+sc_y/2)
        
        ]) + np.array([(sc_x/2,sc_y/2)])
        
        self._statemachine = {
            "done": False,
            "face":0,
            "eyes": 0,
            "capturing": False,
        }
        
    def _update_state(self):
        
        # is currently idle
        # is already positioned, should start capturing
        if not self._statemachine['capturing']:
            #start capturing
            print("cap")
            self._statemachine['capturing'] = True
            return
            
        # is currently capturing data
        # should stop and skip to next statemachine entries
        if self._statemachine['capturing']:
            # stop capturing
            print("no cap")
            self._statemachine['capturing'] = False
            if self._statemachine['eyes'] >= len(self._screen_pos) - 1:
                self._statemachine['eyes'] = 0
                self._statemachine['face'] += 1
            else:
                self._statemachine['eyes'] +=1
            
            if self._statemachine['face'] >= len(self._screen_pos) - 1:
                print("Done all training")
                self._statemachine['done']=True
            return
        
    def save_training(self):
        #save the complete version
        #self.df_feat.to_json('database/df_compl_'+self.name+'.json')
        
        info = pd.DataFrame(columns=['feature','shape'])
        #save the name+shape
        for i in range(len(self.df_feat.columns)):
            add1 = pd.DataFrame([[self.df_feat.columns[i],np.array(self.df_feat.iloc[0,i]).shape]],columns=['feature','shape']) # type: ignore
            info = pd.concat([info,info,add1],ignore_index=True)
        
        info.to_json('database/db_info_'+self.name+'.json')
        
        flattened = pd.DataFrame([ [np.concatenate([ col.flatten() for col in line]).tolist()] for _,line in self.df_feat.iloc[:,0:4].iterrows() ],columns=['data'])
        flattened.insert(loc=len(flattened.columns),column='target',value=self.df_feat.iloc[:,4])
        flattened.to_json('database/df_flat_'+self.name+'.json')
        
        #self.df_feat.to_sql('database/df_'+self.name+'.csv')
        #self.df_feat = pd.read_csv('data/testmdl.csv')
        
    def stageEvents(self,evl = [pg.event.Event]):
        #window event
        #get spacebar pressed
        #next stage on drawing
        for event in evl:
            print(event)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_q)):
                self.cam_instance.stop_worker()
                self.wnd.stop_worker()
                #self.done = True
                self.save_training()
                
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                #next_stage
                print("nextstage")
                self._update_state()

    def start(self):
        self.wnd.start_worker()
        self.cam_instance.stop_worker()
    
    def drawing(self):
        pg.draw.rect(self.wnd.screen, dark_red, pg.Rect(SCREEN_SIZE[0]/2 - 30, SCREEN_SIZE[1]/2 - 30, 60, 60))
        
        my_font = pg.font.SysFont('Verdana', 30)
        if self._statemachine['done']:
            text_surface = my_font.render('All Done :)', False, (0, 0, 0))
            self.wnd.screen.blit(text_surface, (SCREEN_SIZE[0]/2 - 80,SCREEN_SIZE[1]/2 - 90))
        else:
            if self._statemachine['capturing']:
                text_surface = my_font.render('Currently capturing', False, (0, 0, 0))
                self.wnd.screen.blit(text_surface, (SCREEN_SIZE[0]/2 - 60,SCREEN_SIZE[1]/2 - 90))
            else:
                text_surface = my_font.render('Align with the markings for capture', False, (0, 0, 0))
                self.wnd.screen.blit(text_surface, (SCREEN_SIZE[0]/2 - 130,SCREEN_SIZE[1]/2 - 90))
        
        
            # blue circle you are supposed to point your face at
            pg.draw.circle(self.wnd.screen,
                        (94,174,235),
                        tuple(self._screen_pos[self._statemachine['face']].tolist()),
                        40.0,1
                        )
            # green circle you are supposed to look at
            pg.draw.circle(self.wnd.screen,
                        (55,255,119),
                        tuple(self._screen_pos[self._statemachine['eyes']].tolist()),
                        30.0,1
                        )
            
            #if type(self.drawn) is not NoneType:
                ##cv.imshow('mask1',self.cam_instance.mask1)
                #frame = cv.cvtColor(self.cam_instance.mask1, cv.COLOR_BGR2RGB)
                #frame = np.rot90(frame)
                #self.wnd.screen.blit(pg.surfarray.make_surface(frame), (90, 0))
            
            #draw center
            #animations
            #   directions: center, W, E, N, S, NW, NE, SW, SE
            
            #   directions for: [eye,face]
        pass

    def caller(self,*cam_feats):
        #camera has a new frame to register
        #get the features
        #get the coordinates
        if self._statemachine['capturing']:
            #start storing data
            #cam_feats[0]
            add1 = pd.DataFrame(cam_feats, columns=["im2Dface_center","im3Dface_dir","diff_left","diff_right"])
            add1.insert(loc=len(add1.columns), column='iris_pos', value=[self._screen_pos[self._statemachine['eyes']].tolist()])
            self.df_feat = pd.concat([self.df_feat,add1], ignore_index=True)
            
            
            
            
            
            
            
class Tracker:
    def __init__(self,name: str):
        
        self.name = name
        self.scr_coords = (0,0)
        
        #create camera object
        #create Window object
        
        self.mdl = load_training_model(name)
        self.cam_instance = CamTrack()
        self.cam_instance.set_featureFetch(self.caller)
        
        #draw/write on window
        self.wnd = CompWindow(self.drawing,self.stageEvents)
        
        #start workers
        print("start workers")
        self.cam_instance.start_worker()
        print("start cam worker")
        
        sc_x = SCREEN_SIZE[0]/2
        sc_y = SCREEN_SIZE[1]/2
        
        # o canto superior esquerdo tá no centro!!!
        # tem que ajustar /remover 0.3
        # tem q ver o output disso
        # tem q fazer um seletor de camera
            # fazer um "detector de face"
            # perguntar se pode abrir imagem no opencv em uma janelinha
        self._tracker_pos = lambda: (sc_x + self.scr_coords[0]*0.3,sc_y + self.scr_coords[1]*0.3)
        
        
    def stageEvents(self,evl = [pg.event.Event]):
        #window event
        #get spacebar pressed
        #next stage on drawing
        for event in evl:
            print(event)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_q)):
                self.cam_instance.stop_worker()
                self.wnd.stop_worker()
                #self.done = True
                
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                #next_stage
                print("?")

    def start(self):
        self.wnd.start_worker()
        self.cam_instance.stop_worker()
    
    def drawing(self):
        pg.draw.rect(self.wnd.screen, dark_red, pg.Rect(SCREEN_SIZE[0]/2 - 30, SCREEN_SIZE[1]/2 - 30, 60, 60))
        # blue circle where you are looking
        pg.draw.circle(self.wnd.screen,(94,174,235),self._tracker_pos(),40.0,1)

    def caller(self,*cam_feats):
        #send it to the model
        #print(cam_feats)
        #otimizar isso aqui!!!!
        dbfeat = pd.DataFrame(cam_feats, columns=["im2Dface_center","im3Dface_dir","diff_left","diff_right"])
        flattened = pd.DataFrame([ [np.concatenate([ col.flatten() for col in line]).tolist()] for _,line in dbfeat.iloc[:,0:4].iterrows() ],columns=['data'])
        x_train_feats = pd.DataFrame(flattened.iloc[:,0])
        x_train_feats = pd.DataFrame(x_train_feats['data'].tolist(),index=flattened.index)
        prediction = self.mdl.predict(x_train_feats)
        
        self.scr_coords = tuple(prediction[0])
        #print(self.scr_coords)
        
        """ if self._statemachine['capturing']:
            #start storing data
            #cam_feats[0]
            add1 = pd.DataFrame(cam_feats, columns=["im2Dface_center","im3Dface_dir","diff_left","diff_right"])
            add1.insert(loc=len(add1.columns), column='iris_pos', value=[self._screen_pos[self._statemachine['eyes']].tolist()])
            self.df_feat = pd.concat([self.df_feat,add1], ignore_index=True)
             """