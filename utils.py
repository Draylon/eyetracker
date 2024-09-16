import threading
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


#====================================================

import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

def compose_model_db(name:str):
    df = pd.read_json("database/df_flat_"+name+".json")
    
    ##read the dataframe file, flatten it and feed it to the AI @ the core
    ##probably should move this bit into the core @ utils.py
    #flattened = pd.DataFrame([ [np.concatenate([ col.flatten() for col in line]).tolist()] for _,line in df.iloc[:,0:4].iterrows() ],columns=['data'])
    ##flattened.insert(loc=len(flattened.columns),column='target',value=df.iloc[:,4])
    #targ = pd.DataFrame(df.iloc[:,4],columns=['target'])
    #return flattened,targ
    x_train_feats = pd.DataFrame(df.iloc[:,0])
    x_train_feats = pd.DataFrame(x_train_feats['data'].tolist(),index=df.index)
    
    y_train_points = pd.DataFrame(df.iloc[:,1])
    y_train_points = pd.DataFrame(y_train_points['target'].tolist(),index=df.index)
    
    return create_model(name=name,entries=df.iloc[0,0].__len__(),x_train_feats=x_train_feats,y_train_points=y_train_points) # type: ignore
    #create_model(name=name,entries=len(flattened.columns),x_train_feats=flattened,y_train_points=targ)

def create_model(name:str,entries:int,x_train_feats:pd.DataFrame,y_train_points:pd.DataFrame):
    model = Sequential()
    model.add(Dense(128, input_shape=(entries,), activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    checkpoint = ModelCheckpoint("model/"+name+'_mdl_best.keras',save_weights_only=False, monitor='val_loss', save_best_only=True)
    
    model.fit(x_train_feats, y_train_points, epochs=500, batch_size=32, validation_split=0.2,callbacks=[checkpoint])
    model.save("model"+name+'_mdl.keras')
    
    #predicted_2d = model.predict(new_input_features)
    return model

def load_training_model(name):
    return load_model(name+'_mdl.h5')