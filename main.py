import sys

params = sys.argv[1:]
#pairs = [(params[a],params[a+1]) for a in range(0,len(params),2)]

for i,p in enumerate(params):
    if p == "create":
        #logic:
        # if param i+1 (<name>) is provided, create a database and
        # a model with the parameter, otherwise create a custom name
        
        train1 = Training()
        train1.wait()
        # get the training "scene"
        # insert the scene 

        #tasks:
        #gather database
        #save database
        #train model
        #save model
        #close
        pass
    elif p=="load":
        #logic:
        # if param i+1 (<name>) is provided, load the specific, otherwise
        # load the most recent model (search for custom name, then search the folder)

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