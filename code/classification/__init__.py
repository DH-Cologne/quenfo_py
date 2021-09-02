""" Script to handle the classification.
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs """

# ## Imports
from sqlalchemy.orm import query
from classification.prepare_classifyunits import generate_classifyunits
from database import session
from orm_handling import orm
from training.train_models import Model
import logging
from classification import predict_classes
from configuration.config_model import Configurations
import gc

# ## Function
def classify(model: Model) -> None:
    """ Classify JobAds
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs 

    Parameters
    ----------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # ## Set Variables
    # query_limit: Number of JobAds to process
    query_limit = Configurations.get_query_limit()
    # start_pos: Row Number where to start query
    start_pos = Configurations.get_start_pos()
    # set row number for query
    query_start = start_pos
    # set jobad counter
    counter = 0
        
    while counter < query_limit:

        # STEP 1: Load the Input data: JobAds in JobAds Class.
        jobads = orm.get_jobads(query_start)

        # iterate over each jobad
        for jobad in jobads:

            # STEP 2: Generate classify_units, feature_units and feautre_vectors for each JobAd.
            generate_classifyunits(jobad, model)
                    
            # STEP 3: Predict Classes for CUs in JobAds. 
            predict_classes.start_prediction(jobad, model)

            # add obj to current session --> to be written in db
            orm.create_output(session, jobad)

        # Commit generated classify units with paragraphs and classes to table
        orm.pass_output(session)

        counter += len(jobads)
        query_start += len(jobads)

    
    # Reset traindata changes (used as filler)
    orm.handle_td_changes(model)
    # Close session
    orm.close_session(session)
    