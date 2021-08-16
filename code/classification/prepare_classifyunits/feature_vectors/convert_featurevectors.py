from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import numpy as np


is_created = None
bow_train = ''
clf = ''
fitter =''
all_features = list()
all_classes=list()
import sys


def initialize_bow_train(traindata):
    global is_created
    global bow_train
    global clf
    global fitter
    global all_classes
    global all_features

    if is_created is None:
        print("HELLO")
        for train_obj in traindata:
            for cu in train_obj.children2:
                #df = df.append([{'id':cu.id, 'classID': cu.classID, 'parent': cu.parent2, 'fus': cu.featureunits}], ignore_index=True)
                all_features.append(cu.featureunits)
                all_classes.append(cu.classID)
        
        fitter = TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit(all_features)
        bow_train = fitter.transform(all_features)
        print(bow_train)
        # knn prototyp
        knn = KNeighborsClassifier(n_neighbors=5)
        print(all_classes)
        clf = knn.fit(bow_train, all_classes)
        is_created = 'checked' 
        return clf, fitter
    else:
        return clf, fitter
    
    
def gen_bow_cu(fus, fitter):

    # nur die folgende Zeile hier, dann läuft mit tfidf
    bow_cu = fitter.transform([fus])

    return bow_cu
