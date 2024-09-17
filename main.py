import sys
import datetime
from core import Tracker
from utils import compose_model_db

params = sys.argv[1:]
#pairs = [(params[a],params[a+1]) for a in range(0,len(params),2)]
#params = ["create", "ayylmao"]

def build_name(params,i):
    name = None
    try:
        name = params[i+1]
    except Exception as _: pass
    if name == None:
        name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
    return name

for i,p in enumerate(params):
    if p == "create":
        #logic:
        name = build_name(params,i)
        # if param i+1 (<name>) is provided, create a database and
        # a model with the parameter, otherwise create a custom name
        
        # get the training "scene"
        # insert the scene 
        
        #tasks:
        #gather database
        #save database
        print("start Training")
        from core import Training
        train1 = Training(name=name)
        train1.start()
        print("done Training")
        
        #train model
        
        print("creating model")
        model1 = compose_model_db(name=name)
        print("model created")
        
        
        #save model
        #close
        pass
    elif p=="load":
        #logic:
        # if param i+1 (<name>) is provided, load the specific, otherwise
        # load the most recent model (search for custom name, then search the folder)
        name = build_name(params,i)
        tr1 = Tracker(name=name)
        tr1.start()

        #tasks:
        #start the overlay
        #start the model
        #input the facial features
        #draw the CNN in overlay
        #loop
        pass
    elif p=="recalibrate":
        #logic:
        # if param i+1 (<name>) is provided, load the specific database for more inputs,
        # otherwise load the most recent model (search for custom name, then search the folder)

        #tasks:
        #build an additional database
        #filter for outliers in the data
        #train the model again and save
        #close
        pass
    