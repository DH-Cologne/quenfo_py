"""Main Script of the application. Manages the processes and interactions.

TODO: 
    * General Modifications: config, argparse, requirements
    * Tool separations: Text-Classification, Modeling, ORM-handling etc.
    * Information Extraction and Matching"""

# ## Imports
from prepare_classifyunits import generate_classifyunits
from database import session
from ORM_structure import orm
from ORM_structure.models import ClassifyUnits
from database import engine
import logging

""" # ## Initiate Logging-Module
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename='logger.log', filemode='w+',
) """


# Load the Input data: JobAds in JobAds Class.
jobads = orm.get_jobads(session)

for jobad in jobads:

    # ## TODO: PREPARE CLASSIFY UNITS
    # Pass list of JobAds-objects to be converted to clean paragraphs, featureunits and feature vectors
    generate_classifyunits(jobad)


    # TODO: TEXTCLASSIFICATION
    # Pass cleaned and vectorized jobad to Text-Classification via KNN
    # child is a classify unit for a specific jobad
    """ for child in jobad.children:
        print(child.paragraph)
        print(child.featureunit) 
        print(child.featurevector) """


    # erst nach der Text-classification soll jede jobad inkl. cu mit classID in den output geschrieben werden.
    # add obj to current session --> to be written in db
    orm.create_output(session, jobad)



# Commit generated classify units with paragraphs and class assignments to table
orm.pass_output(session)
session.flush()
session.close()


""" # Load traindata and store it in list of objects
data = use_traindata()

for obj in data:
    # preprocess each obj
    print(obj)
    onestring = manipulate_data(obj)
    # write output
    generate_output(obj, onestring)

# commit sollte besser in orm.py aber dann wirds mehrmals aufgerufen deshalb erstmal hier.
session.commit() """