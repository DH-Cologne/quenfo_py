"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports
from re import I
from . import converter
from database import session
from ORM_structure import orm
from ORM_structure.models import ClassifyUnits
from itertools import zip_longest as izip
from itertools import tee, islice, chain
import sys


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
        # 3. Make feature units
        fu = __get_featureunits(para)

        # 4. Make featurevectors
        fv = __get_featurevectors(fu)

        # 5. Add whitespace free paragraph, default classID, featureunit (ngram list) and featurevector to classify unit
        cu = ClassifyUnits(paragraph=para, classID=0, featureunit=fu, featurevector=fv)
        
        # 6. Connect the cu (classifyunit) as a child to its parent (jobad)
        jobad.children.append(cu)



def __get_paragraphs(jobad: object) -> list:
    # Iterate over all jobad-objects in jobads-list containing the jobad-objects
    #for jobad in jobads:
    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = converter.split_at_empty_line(jobad)
    
    # Remove whitespaces
    list_paragraphs = converter.remove_whitespaces(list_paragraphs)

    return list_paragraphs


def __clean_paragraphs(list_paragraphs: list) -> list:

    # ################### !!! Merge ListIitems nochmal in funktion packen
    cleaned_merged = list()
    i = 1
    list_paragraphs.insert(0, '')
    list_paragraphs.append('')
    previous_to_remember = ''

    while i < len(list_paragraphs):
        # set variables to compare
        para = list_paragraphs[i]
        previous = list_paragraphs[i-1]

        # Merge Listitems together
        para, previous_to_remember = converter.merge_listitems(previous, para, previous_to_remember)

        cleaned_merged.append(para)
        i += 1
    #sys.exit()
    cleaned_merged = list(filter(None, cleaned_merged))

    # #################### !!! Merge what belongs together nochmal in funktion packen
    # TODO: Merge what belongs together (startswith uppercase, endswith period, is jobtitle)
    i = 1
    cleaned_merged.insert(0, '')
    cleaned_merged.append('')
    previous_to_remember = ''
    belongs = []
    while i < len(cleaned_merged):
        # set variables to compare
        para = cleaned_merged[i]
        previous = cleaned_merged[i-1]

        # Merge Listitems together
        para, previous_to_remember = converter.merge_whatbelongstogether(previous, para, previous_to_remember)


        belongs.append(para)
        i += 1

    belongs = list(filter(None, belongs))
    return belongs

# TODO: Rückgabe später sollte kein str sein sonern eine list of strings
def __get_featureunits(para: str) -> str:
    # Ignore all paragraphs without any content
    if para != '':
        # Remove all non alpha-numerical characters
        fu = converter.replace(para)

        # TODO: FEATUREUNIT  
        # normalize, stem, filterSW, nGrams, continousNGrams
        # die fus sollten eine liste bestehend aus strings (den ngrammen sein pro cu eine liste)
        return fu
    else:
        pass

# TODO: rückgabe später sollte kein string sein sondern ein vector
def __get_featurevectors(fu):
    # TODO: FEATUREVECTOR
    # generate featurevector (vorerst vllt mit tfidf)
    fv = ''     # filler
    return fv
