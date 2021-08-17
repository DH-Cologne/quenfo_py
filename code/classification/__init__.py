# ## Imports
import sqlalchemy
from classification.prepare_classifyunits import generate_classifyunits
from database import session, session2
from orm_handling import orm
from orm_handling.models import ClassifyUnits
from database import engine
import logging
import sys
from classification import predict_classes

# hier wird eigentlich das model übergeben
def classify(model):
    # ## STEP 1:
    # Load the Input data: JobAds in JobAds Class.
    jobads = orm.get_jobads(session)

    #generate classify_units, feature_units for Testdata
    for jobad in jobads:
        # ## TODO: PREPARE CLASSIFY UNITS
        # Pass list of JobAds-objects to be converted to clean paragraphs, featureunits and feature vectors
        generate_classifyunits(jobad, model)
        # add obj to current session --> to be written in db
        orm.create_output(session, jobad)
    
    for jobad in jobads:

        predict_classes.start_prediction(jobad, model)
        orm.create_output(session, jobad)


    # Commit generated classify units with paragraphs and class assignments to table
    orm.pass_output(session)
    try:
        orm.delete_filler(session2)
    except sqlalchemy.exc.OperationalError as err:
        print(f'{err}: No need to delete traindata-filler because traindata didnt get processed (model was already there)')
    session.close()