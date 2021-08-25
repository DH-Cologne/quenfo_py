"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports
from orm_handling.models import ClassifyUnits, ClassifyUnits_Train, Model
from . import classify_units
from . import feature_units
from . import feature_vectors


# ### Main-Function for ClassifyUnit generation (+ featureunits and featurevectors)
def generate_classifyunits(jobad: object, model: Model) -> None:
    """ Function manages the preparation for the textclassification. Therefore classifyunits are needed and will be
    generated in this step. Following steps are used: 
        --> Each Jobad is splitted into paragraphs and each paragraph is a value paragraph of the Class ClassifyUnit. 
        --> JobAds and ClassifyUnits are organized in a parent -> children relationship 
        --> One JobAd contains several classifyunits with the following values: 
            a. paragraph = slightly cleaned content (whitespaces at the beginning and the end) 
            b. featureunit = normalized, stemmed, Stopwords filtered and nGrams processed paragraph 
            c. featurevector = vectorized featureunit

    Parameters
    ----------
    jobad: object
        jobad is an object of the class JobAds and contains all given variables 
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # Split the jobad texts (content) and receive a list of paragraphs for each jobad + remove whitespaces
    list_paragraphs = classify_units.get_paragraphs(jobad)

    # Clean each paragraph and merge ListItems and WhatBelongsTogether
    list_paragraphs = classify_units.clean_paragraphs(list_paragraphs)

    # Iterate over each paragraph in list_paragraphs for one jobad
    for para in list_paragraphs:

        """ Remove all non-alphanumerical characters from para and return fus. 
        A lot of fus will be empty lists afterwards, so only ClassifyUnits for filled
        fus are instantiated."""
        fus = feature_units.convert_featureunits.replace(para)

        # Check if fus is an empty list or if child does not exists
        if not(any(para == v.paragraph for v in jobad.children)) and fus != []:
            # Add cleaned paragraph, default classID, featureunits and featurevectors to classify unit
            cu = ClassifyUnits(classID=0, paragraph=para, featureunits=list(), featurevector=list())
            # set the list of token without non-alphanumerical characters as prototype-fus
            cu.set_featureunits(fus)
            # Connect the cu (classifyunit) as a child to its parent (jobad)
            jobad.children.append(cu)
        #if paragraph is already processed in a classifyunit --> store it again at the same place (to avoid duplicates)
        else:
            if fus != []:
                for child in jobad.children:
                    if child.paragraph == para :
                        child.set_featureunits(fus)

    # Iterate over each jobad and make featureunits and featurevectors vor each cu
    for cu in jobad.children:
        # Generate featureunits
        feature_units.get_featureunits(cu)
        # Generate featurevectors
        feature_vectors.get_featurevectors(cu, model)

# Generate ClassifyUnits_Train (and fus) for Trainingdata JobAds
def generate_train_cus(train_obj: object) -> None:
    """ Function to generate CUs for Trainingdata JobAds
        --> No split into paragraphs needed

    Parameters
    ----------
    train_obj: object
        train_obj is an object of the class TrainData """

    # Set paragraph variable
    para = train_obj.content
    
    """ Remove all non-alphanumerical characters from para and return fus. 
        A lot of fus will be empty lists afterwards, so only ClassifyUnits_Train for filled
        fus are instantiated."""
    fus = feature_units.convert_featureunits.replace(para)

    # Check if fus is an empty list or if child does not exists
    if fus != []:
        # Add cleaned paragraph, default classID, featureunits and featurevectors to classify unit
        cu = ClassifyUnits_Train(classID=train_obj.classID, content=para, featureunits=list(), featurevector=list())
        # set the list of token without non-alphanumerical characters as prototype-fus
        cu.set_featureunits(fus)
        # Connect the cu (classifyunit_train) as a child to its parent (TrainData)
        train_obj.children2.append(cu)
        # Generate featureunits
        feature_units.get_featureunits(cu)