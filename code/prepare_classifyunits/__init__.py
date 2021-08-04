"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports

import orm_handling
from orm_handling.models import ClassifyUnits, ClassifyUnits_Train, JobAds
import sys
from . import classify_units
from . import feature_units
from . import feature_vectors


# ### Main-Function for ClassifyUnit generation (+ featureunits and featurevectors)
def generate_classifyunits(jobad: object):
    """ Function manages the preparation for the textclassification. Therefore classifyunits are needed and will be
    generated in this step. Following steps are used: --> Each Jobad is splitted into paragraphs and each paragraph
    is a value paragraph of the Class ClassifyUnit. --> JobAds and ClassifyUnits are organized in a parent -->
    children relationship --> One JobAd contains several classifyunits with the following values: a. paragraph =
    slightly cleaned content (whitespaces at the beginning and the end) b. featureunit = normalized, stemmed,
    Stopwords filtered and nGrams processed paragraph c. featurevector = vectorized featureunit

    Parameters
    ----------
    jobad: object
        jobad is an object of the class JobAds and contains all given variables """

    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad + remove whitespaces
    list_paragraphs = classify_units.get_paragraphs(jobad)

    # 2. Clean each paragraph and merge ListItems and WhatBelongsTogether
    list_paragraphs = classify_units.clean_paragraphs(list_paragraphs)

    # Iterate over each paragraph in list_paragraphs for one jobad
    for para in list_paragraphs:

        """ Remove all non-alphanumerical characters from para and return fus. 
        A lot of fus will be empty lists afterwards, so only ClassifyUnits for filled
        fus are instantiated."""
        fus = feature_units.convert_featureunits.replace(para)

        # Check if fus is an empty list or if child does not exists
        if not(any(para == v.paragraph for v in jobad.children)) and fus != []:
            # 3. Add cleaned paragraph, default classID, featureunits and featurevectors to classify unit
            cu = ClassifyUnits(classID=0, paragraph=para, featureunits=list(), featurevectors=list())
            # set the list of token without non-alphanumerical characters as prototype-fus
            cu.set_featureunits(fus)
            # 4. Connect the cu (classifyunit) as a child to its parent (jobad)
            jobad.children.append(cu)
        #if paragraph is already processed in a classifyunit --> store it again at the same place (to avoid duplicates)
        else:
            if fus != []:
                for child in jobad.children:
                    if child.paragraph == para :
                        child.set_featureunits(fus)


    # Iterate over each jobad and make featureunits and featurevectors vor each cu
    for cu in jobad.children:

        # 5. Make feature units
        feature_units.get_featureunits(cu)

        # Prepare fuso list (unique and ordered vocab of testdata)
        fuso_list = feature_vectors.gen_fuso(cu.featureunits)
    return fuso_list


def generate_train_cus(train_obj):
    para = train_obj.content
    
    fus = feature_units.convert_featureunits.replace(para)

    # Check if fus is an empty list or if child does not exists
    if fus != []:
        # 3. Add cleaned paragraph, default classID, featureunits and featurevectors to classify unit
        cu = ClassifyUnits_Train(classID=0, content=para, featureunits=list(), featurevectors=list())
        # set the list of token without non-alphanumerical characters as prototype-fus
        cu.set_featureunits(fus)
        # 4. Connect the cu (classifyunit) as a child to its parent (jobad)
        train_obj.children2.append(cu)

    
    for cu in train_obj.children2:

        # 5. Make feature units
        feature_units.get_featureunits(cu)



def generate_featurevectors(jobad, fuso_list, traindata):

    for cu in jobad.children:

        # 6. Make featurevectors
        feature_vectors.get_featurevectors(cu, fuso_list, traindata)

    
    #sys.exit()