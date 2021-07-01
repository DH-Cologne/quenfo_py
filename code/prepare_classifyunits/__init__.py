"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports
from re import I
from . import convert_classifyunits
from . import convert_featureunits
from database import session
from ORM_structure import orm
from ORM_structure.models import ClassifyUnits, JobAds
from itertools import zip_longest as izip
from itertools import tee, islice, chain
import sys
from pathlib import Path
import yaml

# ## Open Configuration-file and set paths to models (trained and retrained)
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    fus_config = cfg['fus_config']
   
# ### Main-Function of the Script
def generate_classifyunits(jobad: object):
    """ Function manages the preparation for the textclassification. Therefore classifyunits are needed and will be generated in this step.
        Following steps are used:
        --> Each Jobad is splitted into paragraphs and each paragraph is a value paragraph of the Class ClassifyUnit.
        --> JobAds and ClassifyUnits are organized in a parent --> children relationship
        --> One JobAd contains several classifyunits with the following values:
            a. paragraph = slightly cleaned content (whitespaces at the beginning and the end)
            b. featureunit = normalized, stemmed, Stopwords filtered and nGrams processed paragraph
            c. featurevector = vectorized featureunit

    Parameters
    ----------
    jobad: object
        jobad is an object of the class JobAds and contains all given variables """

    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad + remove whitespaces
    list_paragraphs = __get_paragraphs(jobad)

    # 2. Clean each paragraph and merge ListItems and WhatBelongsTogether
    list_paragraphs = __clean_paragraphs(list_paragraphs)

    # Iterate over each paragraph in list_paragraphs for one jobad
    for para in list_paragraphs:

        """ Remove all non-alphanumerical characters from para and return fus. 
        A lot of fus will be empty lists afterwards, so only ClassifyUnits for filled
        fus are instantiated."""
        fus = convert_featureunits.replace(para).split()

        # Check if fus is a empty list
        if fus != []:
            # 3. Add cleaned paragraph, default classID, featureunits and featurevectors to classify unit
            cu = ClassifyUnits(classID=0, paragraph=para, featureunits=list(), featurevectors=list())
            # set the list of token without non-alphanumerical characters as prototype-fus
            cu.set_featureunits(fus)
            # 4. Connect the cu (classifyunit) as a child to its parent (jobad)
            jobad.children.append(cu)

    # Iterate over each jobad and make featureunits and featurevectors vor each cu
    for cu in jobad.children:
        
        # 5. Make feature units
        __get_featureunits(cu)
        
        # 6. Make featurevectors
        __get_featurevectors(cu)
        


def __get_paragraphs(jobad: object) -> list:
    """ 
    Step 1: Split at emtpy line
        --> Splits the text in jobad.content into Paragraphs at empty lines
    
    Step 2: remove whitespaces
        --> Removes whitespaces at the end and the beginning of a paragraph and each line
   
    
    Parameters
    ----------
    jobad: object
        object of the class JobAds which contains id, posting_id, jahrgang, language, content
    
    Returns
    -------
    list_paragraphs: list
        list with paragraphs for one jobad item """

    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = convert_classifyunits.split_at_empty_line(jobad)
    
    # 2. # Remove whitespaces at the beginning and at the end of each paragraph and in each line
    list_paragraphs = convert_classifyunits.remove_whitespaces(list_paragraphs)

    # Returns organized paragraphs for a jobad
    return list_paragraphs


def __clean_paragraphs(list_paragraphs: list) -> list:
    """ 
    Step 3: identify_listitems: 
    Iterate over a list of paragraphs and compare one paragraph to the previous one. If both paragraphs contain certain list-characters
    (like * or _), the paragraphs are merged together to one paragraph.
    
    Step 4: identify_whatbelongstogether:
    Iterate over a list of paragraphs and compare one paragraph to the previous one. 
    If the previous one ends with a period and the current one starts with uppercase/isjobtitle both paragraphs are merged together to one paragraph.
    
    Parameters
    ----------
    list_paragraphs: list
        list with paragraphs for one jobad item
    
    Returns
    -------
    list_paragraphs: list
        list with better cleaned paragraphs for one jobad item """

    # ## Step 3: to merge ListItems Together
    list_paragraphs = convert_classifyunits.identify_listitems(list_paragraphs)

    # ## Step 4: to merge What Belongs Together
    list_paragraphs = convert_classifyunits.identify_whatbelongstogether(list_paragraphs)

    # return cleaned list (listitems and belongs) to generate_classifyunits()
    return list_paragraphs


def __get_featureunits(cu: object) -> str:

    # TODO: FEATUREUNIT  
    # normalize, stem, filterSW, nGrams, continousNGrams
    fus = convert_featureunits.normalize(cu.featureunits, fus_config['normalize'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.stem(cu.featureunits, fus_config['stem'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.filterSW(cu.featureunits, fus_config['filterSW'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.ngrams(cu.featureunits, fus_config['nGrams'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.cngrams(cu.featureunits, fus_config['continousNGrams'])
    cu.set_featureunits(fus)



# TODO: rückgabe später sollte kein string sein sondern ein vector
def __get_featurevectors(cu):
    fvs = cu.featureunits

    # TODO: FEATUREVECTOR
    # generate featurevector (vorerst vllt mit tfidf)
    fvs = 'filler'    # filler
    cu.set_featurevectors(fvs)
