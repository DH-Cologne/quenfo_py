"""Main Script of the application. Manages the processes and interactions.

TODO: 
    * General Modifications: config, argparse, requirements
    * Tool separations: Text-Classification, Modeling, ORM-handling etc.
    * Information Extraction and Matching"""

# ## Imports
from classification.prepare_classifyunits import  generate_train_cus
from database import session, session2
from orm_handling import orm
from orm_handling import models
from orm_handling.models import ClassifyUnits
from database import engine
import logging
import sys
from classification import classify
from training import initialize_model

""" # ## Initiate Logging-Module
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename='logger.log', filemode='w+',
) """

model = initialize_model()
#traindata = train()

classify(model)



