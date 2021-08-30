""" Main Script of the application. Manages the main components of the tool. """

# ## Imports
from classification import classify
from training import initialize_model
import logging
from pathlib import Path


# ## Initiate Logging-Module for Classification
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename=Path('logging/logger_classification.log'), filemode='w+',
)

# STEP 1: Train or Load Vectorizer a KNN as Class-object model
model = initialize_model()

# STEP 2: Start Classification
classify(model)

# STEP 3a: Information Extraction 
# STEP 3b: Matching 


# TODO: ArgumentParser für step modeling + classify, information extraction, matching


