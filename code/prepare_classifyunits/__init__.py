"""Script to split jobads into paragraphs and generate classifyunits for each paragraphs."""

# ## Imports
from . import converter
from database import session
from ORM_structure import orm
from ORM_structure.models import ClassifyUnits

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
    # 2. Clean each paragraph
    for para in list_paragraphs:
        para = __clean_paragraphs(para)
        # 3. Make feature units
        fu = __get_featureunits(para)
        if fu != '':
            # 4. Make featurevectors
            fv = __get_featurevectors(fu)

            # 5. Add whitespace free paragraph, default classID, featureunit (ngram list) and featurevector to classify unit
            cu = ClassifyUnits(paragraph=para, classID=0, featureunit=fu, featurevector=fv)
            
            # 6. Connect the cu (classifyunit) as a child to its parent (jobad)
            jobad.children.append(cu)
            
            # ## Some Print-Statements for checking
            # prints the related parent id for a child
            # print(cu.parent.id)
            # prints each child with the classifyunits id and the related parent id
            #print(cu)
        else:
            pass


def __get_paragraphs(jobad: object) -> list:
    # Iterate over all jobad-objects in jobads-list containing the jobad-objects
    #for jobad in jobads:
    # 1. Split the jobad texts (content) and receive a list of paragraphs for each jobad
    list_paragraphs = converter.split_at_empty_line(jobad)
    return list_paragraphs


def __clean_paragraphs(para: str) -> str:
    # Remove spaces at the beginning and at the end of the string
    para = converter.remove_whitespaces(para)
    return para

# TODO: Rückgabe später sollte kein str sein sonern eine list of strings
def __get_featureunits(para: str) -> str:
    # Remove all non alpha-numerical characters
    fu = converter.replace(para)
    # Ignore all paragraphs without any content
    if fu != '':
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
