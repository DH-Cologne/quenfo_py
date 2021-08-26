""" Script to handle the classification.
    * Step 1: Load JobAds
    * Step 2: Generate CUs (and also fus and fvs) from JobAds
    * Step 3: Predict Classes for CUs """

# ## Imports
from classification.prepare_classifyunits import generate_classifyunits
from database import session
from orm_handling import orm
from orm_handling.models import Model
import logging
from classification import predict_classes
from orm_handling.models import Model

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
    
    # STEP 1: Load the Input data: JobAds in JobAds Class.
    jobads = orm.get_jobads()

    # STEP 2: Generate classify_units, feature_units and feautre_vectors for each JobAd.
    for jobad in jobads:
        # Pass list of JobAds-objects to be converted to clean paragraphs, feature_units and feature_vectors
        generate_classifyunits(jobad, model)
        # add obj to current session --> to be written in db
        orm.create_output(session, jobad)
    
    # STEP 3: Predict Classes for CUs in JobAds.
    for jobad in jobads:
        predict_classes.start_prediction(jobad, model)
        orm.create_output(session, jobad)

    # Commit generated classify units with paragraphs and classes to table
    orm.pass_output(session)
    # Reset traindata changes (used as filler)
    orm.handle_td_changes(model)
    # Close session
    orm.close_session(session)