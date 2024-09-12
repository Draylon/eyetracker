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
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

def create_model(name:str,entries:int,x_train_feats:pd.DataFrame,y_train_points:pd.DataFrame):
    model = Sequential()
    model.add(Dense(128, input_dim=entries, activation='relu'))  # input_dim is the number of input coordinates
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2))
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    checkpoint = ModelCheckpoint(name+'_mdl_best.h5', monitor='val_loss', save_best_only=True)
    
    model.fit(x_train_feats, y_train_points, epochs=500, batch_size=32, validation_split=0.2,callbacks=[checkpoint])
    model.save(name+'_mdl.h5')
    
    #predicted_2d = model.predict(new_input_features)


def load_training_model(name):
    return load_model(name+'_mdl.h5')