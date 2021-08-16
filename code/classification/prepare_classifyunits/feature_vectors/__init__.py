from orm_handling.models import JobAds, TrainingData
from . import convert_featurevectors
import itertools
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer

#fuso_list = list()

""" def gen_fuso(fus):
    # packe die ngramme der fus in eine liste um ein unique vocab zu erhalten
    # noch kommen hier rund 20.000 raus, bei java rund 10.000 ngramme/features warum?   
    global fuso_list

    fuso_list.extend(fu for fu in fus)
    
    # better way to remove duplicates and order list items alphabetically
    fuso_list = sorted(list(dict.fromkeys(fuso_list)))

    return fuso_list """

# TODO: rückgabe später sollte kein string sein sondern ein vector
def get_featurevectors(cu: object, traindata: list):

    """
    INPUT:
        b. traindata: as ngram set
        c. testdata current object
        
        aus cu wird das bow1, aus traindata wird das bow2 und das bowtemp"""

    clf, fitter = convert_featurevectors.initialize_bow_train(traindata)

    # dann bow1 erstellt und mit featureuntis gefüllt und zum multisets
    bow_cu = convert_featurevectors.gen_bow_cu(cu.featureunits, fitter)
    # dann wird bow_temp = bow_temp - bow1
    
    # prototyp prediction
    predicted = clf.predict(bow_cu)
    print(cu, predicted)
    
    cu.set_classID(predicted[0])