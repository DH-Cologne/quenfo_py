from orm_handling.models import JobAds, TrainingData
from . import convert_featurevectors
import itertools
import sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer


# TODO: rückgabe später sollte kein string sein sondern ein vector
def get_featurevectors(cu: object, model):

    """
    INPUT:
        b. traindata: as ngram set
        c. testdata current object
        
        aus cu wird das bow1, aus traindata wird das bow2 und das bowtemp"""

    vectorizer = model.vectorizer

    clf = model.model_knn

    # das bleibt hier
    tfidf_cu = convert_featurevectors.gen_tfidf_cu(cu.featureunits, vectorizer)
    
    # prototyp prediction
    predicted = clf.predict(tfidf_cu)
    print(cu, predicted)
    
    cu.set_classID(predicted[0])