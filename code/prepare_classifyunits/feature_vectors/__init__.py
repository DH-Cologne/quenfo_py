from orm_handling.models import JobAds, TrainingData
from . import convert_featurevectors
import itertools
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer

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

    # überprüfen ob fuso list gefüllt ist, sonst neu generieren
    # wenn bereits trainiertes modell vorliegt dann liegt auch traindata bow2 schon vor, sonst nochmal füllen

    # bow2 generieren und dann multiset erstellen mögl. mit dictionary vllt --> dict mit featureunits und dann entsprechende anzahl an vorkommen {fu(blume): 3}
    # bow2 ist dann das dictionary#
    bow_train, fitter, clf, all_classes = convert_featurevectors.initialize_bow_train(traindata, cu.featureunits)

    # dann bow_temp = bow2
    bow_temp = bow_train

    # dann bow1 erstellt und mit featureuntis gefüllt und zum multisets
    bow_cu = convert_featurevectors.gen_bow_cu(cu.featureunits, fitter)
    # dann wird bow_temp = bow_temp - bow1

    # prototyp prediction
    predicted = clf.predict(bow_cu)
    print(cu, predicted)
    
    cu.set_classID(predicted[0])


    #bow_temp = np.delete(bow_temp, np.where(bow_temp==bow_cu))


    # aus bow1 und bow_temp wird mittels loglikelihood dann die scores berechnet



    """ # vectorize die trainingsdaten durch bow-fitter und return
    bow_train, all_classes, clf, fitter = convert_featurevectors.initialize_bow_train(traindata, cu.featureunits)

    bow_temp = bow_train
    
    
    # vectorize die cu mittels fitter
    bow_cu = convert_featurevectors.gen_bow_cu(cu.featureunits, fitter) """
    
    #bow_temp = np.delete(bow_train, np.where(bow_train==bow_cu))
    #print(bow_temp)
    


    


    # TODO: REMOVE BOW_CU FROM BOW_TRAIN = BOW_TEMP

    # SEHR ZEITAUFWENDIG
    #bow_temp = np.delete(bow_train, np.where(bow_train==bow_cu))

    """ bow_temp = bow_train
    try:
        bow_temp = np.ndarray(list(bow_train).remove(bow_cu)) 
    except ValueError:
        print("bow1 is not part of bowtemp")
        pass """
    

    fvs = 'filler'  # filler

    cu.set_featurevectors(fvs)
