# ## Imports
from classification.prepare_classifyunits import generate_classifyunits, generate_featurevectors, generate_train_cus
from database import session, session2
from orm_handling import orm
from orm_handling.models import ClassifyUnits
from database import engine
import logging
import sys

# hier wird eigentlich das model übergeben
def classify(model):
    # ## STEP 1:
    # Load the Input data: JobAds in JobAds Class.
    jobads = orm.get_jobads(session)

    #generate classify_units, feature_units for Testdata
    for jobad in jobads:
        # ## TODO: PREPARE CLASSIFY UNITS
        # Pass list of JobAds-objects to be converted to clean paragraphs, featureunits and feature vectors
        generate_classifyunits(jobad)
        # add obj to current session --> to be written in db
        orm.create_output(session, jobad)


    # ## STEP 3: 
    # generate Featurevectors for Testdata
    # extra loop because already processed featureunits are needed here
    for jobad in jobads:
        
        # TODO: Check if fuso_list is filled
        generate_featurevectors(jobad, model)

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