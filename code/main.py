"""Main Script of the application. Manages the processes and interactions.

TODO: 
    * General Modifications: config, argparse, requirements
    * Tool separations: Text-Classification, Modeling, ORM-handling etc.
    * Information Extraction and Matching"""

# ## Imports
from prepare_classifyunits import generate_classifyunits, generate_featurevectors, generate_train_cus
from database import session, session2
from orm_handling import orm
from orm_handling.models import ClassifyUnits
from database import engine
import logging

""" # ## Initiate Logging-Module
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename='logger.log', filemode='w+',
) """


# Load the Input data: JobAds in JobAds Class.
jobads = orm.get_jobads(session)

# Load the TrainingData: TrainingData in TrainingData Class
traindata = orm.get_traindata(session2)


# ## PREPARATION 
# STEP 1: generate classify_units, feature_units for Testdata
for jobad in jobads:

    # ## TODO: PREPARE CLASSIFY UNITS
    # Pass list of JobAds-objects to be converted to clean paragraphs, featureunits and feature vectors
    fuso_list = generate_classifyunits(jobad)

    # add obj to current session --> to be written in db
    orm.create_output(session, jobad)



# STEP 2: generate classify_units and feature_units for Traindata

for train_obj in traindata:

    generate_train_cus(train_obj)




# STEP 3: generate Featurevectors for Testdata
# extra loop because already processed featureunits are needed here
for jobad in jobads:
    
    # TODO: Check if fuso_list is filled
    generate_featurevectors(jobad, fuso_list, traindata)

    # add obj to current session --> to be written in db
    orm.create_output(session, jobad)



# TODO: TEXTCLASSIFICATION
    # Pass cleaned and vectorized jobad to Text-Classification via KNN
    # child is a classify unit for a specific jobad
    """ for child in jobad.children:
    print(child.paragraph)
    print(child.featureunit) 
    print(child.featurevector) """
    # working!!!
    """ for cu in jobad.children:
        print(cu.featureunits)
        cu.set_classID(2) """

# Commit generated classify units with paragraphs and class assignments to table
orm.pass_output(session)
orm.delete_filler(session2)
session.close()

