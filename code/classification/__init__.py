""" Script to handle the classification.
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs """

# ## Imports
from . import prepare_classifyunits
from . import predict_classes
import database
from orm_handling import orm
from training.train_models import Model
import logging
import configuration
import sys

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
    query_limit = configuration.config_obj.get_query_limit()
    # start_pos: Row Number where to start query
    start_pos = configuration.config_obj.get_start_pos()
    # set row number for query
    current_pos = start_pos
    # set jobad counter
    counter = 0
    jobad_counter = 0
        
    while True:
        
        # Load the Input data: JobAds in JobAds Class.
        jobads = orm.get_jobads(current_pos)
        
        if len(jobads) == 0:
            break
        elif counter >= query_limit:
            break

        # iterate over each jobad
        for jobad in jobads:
            """ jobad_counter += 1

            if (jobad_counter % 50)==0:
                print((100 *jobad_counter)/query_limit) """

            logging.info(f"before preprocessing in jobad {jobad}")   
            # STEP 2: Generate classify_units, feature_units and feautre_vectors for each JobAd.
            prepare_classifyunits.generate_classifyunits(jobad, model)

            logging.info(f"before prediction in jobad {jobad}")        
            # STEP 3: Predict Classes for CUs in JobAds. 
            predict_classes.start_prediction(jobad, model)

            # add obj to current session --> to be written in db
            orm.create_output(database.session, jobad)
        
        # Commit generated classify units with paragraphs and classes to table
        orm.pass_output(database.session)
        logging.info(f'session is cleaned and every obj is flushed: {database.session._is_clean()}')
        counter += len(jobads)
        current_pos += len(jobads)
        
    
    # Reset traindata changes (used as filler)
    orm.handle_td_changes(model)
    # Close session
    orm.close_session(database.session)