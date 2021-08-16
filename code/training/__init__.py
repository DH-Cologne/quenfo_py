# ## Imports
from classification.prepare_classifyunits import  generate_train_cus
from database import session, session2
from orm_handling import orm
import logging
import sys

def train():
    # ## STEP 2:
    # Load the TrainingData: TrainingData in TrainingData Class
    traindata = orm.get_traindata(session2)

    # generate classify_units and feature_units for Traindata
    for train_obj in traindata:
        generate_train_cus(train_obj)
        
    return traindata