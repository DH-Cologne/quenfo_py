from orm_handling.models import JobAds
from . import convert_featurevectors
import itertools

fuso_list = list()

def gen_fuso(fus):
    # packe die ngramme der fus in eine liste um ein unique vocab zu erhalten
    # noch kommen hier rund 20.000 raus, bei java rund 10.000 ngramme/features warum?   
    global fuso_list

    fuso_list.extend(fu for fu in fus)
    
    # better way to remove duplicates and order list items alphabetically
    fuso_list = sorted(list(dict.fromkeys(fuso_list)))

    # way slower:
    #fuso_list = sorted(set(fuso_list))

    return fuso_list

# TODO: rückgabe später sollte kein string sein sondern ein vector
def get_featurevectors(cu: object, fuso_list: list, traindata: list):

    """
    INPUT:
        a. fuso_list: unique and ordered vocab of the testdata
        b. traindata: as ngram set
        c. testdata current object
        
        aus cu wird das bow1, aus traindata wird das bow2 und das bowtemp"""


    # TODO: FEATUREVECTOR
    #print(len(fuso_list))

    #print(jobads)
    # generate featurevector

    fvs = 'filler'  # filler

    cu.set_featurevectors(fvs)
