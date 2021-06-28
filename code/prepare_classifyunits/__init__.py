"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports
from re import I
from . import converter
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
    fu_config = cfg['fu_config']
   


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

    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = __get_paragraphs(jobad)

    # 2. Clean each paragraph and merge ListItems and WhatBelongsTogether
    list_paragraphs = __clean_paragraphs(list_paragraphs)

    for para in list_paragraphs:
        # 3. Add cleaned paragraph, default classID, featureunit and featurevector to classify unit
        cu = ClassifyUnits(paragraph=para, classID=0, featureunit='', featurevector='')
        
        # 4. Connect the cu (classifyunit) as a child to its parent (jobad)
        jobad.children.append(cu)

    for cu in jobad.children:
        # 5. Make feature units
        fu = __get_featureunits(cu)
        cu.set_featureunit(fu)

        # 6. Make featurevectors
        fv = __get_featurevectors(cu)
        cu.set_featurevector(fv)



def __get_paragraphs(jobad: object) -> list:
    # Iterate over all jobad-objects in jobads-list containing the jobad-objects
    #for jobad in jobads:
    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = converter.split_at_empty_line(jobad)
    
    # Remove whitespaces
    list_paragraphs = converter.remove_whitespaces(list_paragraphs)

    return list_paragraphs


def __clean_paragraphs(list_paragraphs: list) -> list:
    """
    Step 1: identify_listitems: 
    Iterate over a list of paragraphs and compare one paragraph to the previous one. If both paragraphs contain certain list-characters
    (like * or _), the paragraphs are merged together to one paragraph.
    
    Step 2: identify_whatbelongstogether:
    Iterate over a list of paragraphs and compare one paragraph to the previous one. 
    If the previous one ends with a period and the current one starts with uppercase/isjobtitle both paragraphs are merged together to one paragraph.
    """

    def __identify_listitems(list_paragraphs: list) -> list:
        # Set variables
        # List to store cleaned paragraphs
        cleaned_merged = list()
        # counter
        i = 1
        # add an empty string at the beginning and ending of the list for easier iteration
        list_paragraphs.insert(0, '')
        list_paragraphs.append('')
        # set memory variable
        previous_to_remember = str()

        while i < len(list_paragraphs):
            # set variables to compare
            para = list_paragraphs[i]
            previous = list_paragraphs[i-1]

            # Merge Listitems together
            para, previous_to_remember = converter.merge_listitems(previous, para, previous_to_remember)

            # append merged or old paragraph to output list
            cleaned_merged.append(para)
            i += 1
        # remove empty strings
        cleaned_merged = list(filter(None, cleaned_merged))
        return cleaned_merged
    list_paragraphs = __identify_listitems(list_paragraphs)

    def __identify_whatbelongstogether(list_paragraphs: list) -> list:
        # Set variables
        # List to store cleaned paragraphs
        belongs = list()
        # counter
        i = 1
        # add an empty string at the beginning and ending of the list for easier iteration
        list_paragraphs.insert(0, '')
        list_paragraphs.append('')
        # set memory variable
        previous_to_remember = str()
       
        while i < len(list_paragraphs):
            # set variables to compare
            para = list_paragraphs[i]
            previous = list_paragraphs[i-1]

            # Merge Listitems together
            para, previous_to_remember = converter.merge_whatbelongstogether(previous, para, previous_to_remember)

            # append merged or old paragraph to output list
            belongs.append(para)
            i += 1
        # remove empty strings
        belongs = list(filter(None, belongs))
        return belongs

    list_paragraphs = __identify_whatbelongstogether(list_paragraphs)

    # return cleaned list (listitems and belongs) to generate_classifyunits()
    return list_paragraphs

# TODO: Rückgabe später sollte kein str sein sonern eine list of strings
def __get_featureunits(cu) -> str:
    fu = cu.paragraph
    # Remove all non alpha-numerical characters
    fu = convert_featureunits.replace(fu)

    # TODO: FEATUREUNIT  
    # normalize, stem, filterSW, nGrams, continousNGrams
    # Hier auslesen der config und übergabe der parameter an convert_featureunits.configuration?
    fu = convert_featureunits.normalize(fu, fu_config['normalize'])
    fu = convert_featureunits.stem(fu, fu_config['stem'])
    fu = convert_featureunits.filterSW(fu, fu_config['filterSW'])
    fu = convert_featureunits.ngrams(fu, fu_config['nGrams'])
    fu = convert_featureunits.cngrams(fu, fu_config['continousNGrams'])

    # die fus sollten eine liste bestehend aus strings (den ngrammen sein pro cu eine liste) --> anpassen in models.py
    return fu


# TODO: rückgabe später sollte kein string sein sondern ein vector
def __get_featurevectors(cu):
    fv = cu.featureunit

    # TODO: FEATUREVECTOR
    # generate featurevector (vorerst vllt mit tfidf)
    fv = 'filler'    # filler
    return fv
