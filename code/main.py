"""Main Script of the application. Manages the processes and interactions.

TODO: 
    * General Modifications: config, argparse, requirements
    * Tool separations: Text-Classification, Modeling, ORM-handling etc.
    * Information Extraction and Matching"""

# ## Imports

from classification import classify
from training import initialize_model

from orm_handling.models import Configurations

""" # ## Initiate Logging-Module
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename='logger.log', filemode='w+',
) """



# STEP 1: Train or Load Vectorizer and KNN as Class-object model
model = initialize_model()

# STEP 2: Start Classification
classify(model)





