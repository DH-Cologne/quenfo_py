from orm_handling.models import JobAds, TrainingData
from . import convert_featurevectors
import itertools
import sys
import numpy as np

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

    # Adde alle Featureunits der traindata zum bow_train (aka bow2) muss nureinmal gemacht werden
    bow_train = convert_featurevectors.initialize_bow_train(traindata)
    # Adde alle Featureunits der testdaten zuum bow_cu (aka bow1) wird jedes mal neue für jede cu gemacht
    bow_cu = convert_featurevectors.gen_bow_cu(cu.featureunits)

    # TODO: REMOVE BOW_CU FROM BOW_TRAIN = BOW_TEMP
    #bow_temp = bow_train.remove(bow_cu)
    #bow_temp = np.delete(bow_train, np.where(bow_train == bow_cu), axis=0)
    #bow_temp = np.all(np.equal(bow_train, bow_cu), axis=1)
    #bow_temp = np.delete(bow_train,np.where(bow_train==bow_cu))

    # SEHR ZEITAUFWENDIG
    bow_temp = np.delete(bow_train, np.where(bow_train==bow_cu))

    """ bow_temp = bow_train
    try:
        bow_temp = np.ndarray(list(bow_train).remove(bow_cu)) 
    except ValueError:
        print("bow1 is not part of bowtemp")
        pass """
    
    #print(bow_temp)

    #print(bow_temp)

    #sys.exit()
    # TODO: FEATUREVECTOR
    #print(len(fuso_list))

    #print(jobads)
    # generate featurevector

    fvs = 'filler'  # filler

    cu.set_featurevectors(fvs)
