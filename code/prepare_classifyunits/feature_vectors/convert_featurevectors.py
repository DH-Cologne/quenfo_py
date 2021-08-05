from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

import loglikelihood
is_created = None
bow_train = [[]]
clf = ''
df = pd.DataFrame()
fitter =''
all_features = list()
all_classes=list()
all_featuresagain = list()

def initialize_bow_train(traindata, fus):
    global df
    global is_created
    global bow_train
    
    global clf
    global fitter
    global all_classes
    global all_features
    global all_featuresagain
    
    
    if is_created is None:
 
        for train_obj in traindata:
            for cu in train_obj.children2:
                #df = df.append([{'id':cu.id, 'classID': cu.classID, 'parent': cu.parent2, 'fus': cu.featureunits}], ignore_index=True)
                all_features.append(cu.featureunits)
                all_classes.append(cu.classID)
        

        fitter = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit(all_features)
        bow_train = fitter.transform(all_features)

        # knn prototyp
        knn = KNeighborsClassifier(n_neighbors=5)
        
        clf = knn.fit(bow_train, all_classes)
        
        is_created = 'checked'
        return bow_train, all_classes, clf, fitter
    else:
        return bow_train, all_classes, clf, fitter


def gen_bow_cu(fus, fitter):

    #bow_cu = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform([fus])
    bow_cu = fitter.transform([fus])
    #bow_cu = loglikelihood.llr(np.matrix(bow_cu))
    """ tfidf_transformer = TfidfTransformer()
    bow_cu = tfidf_transformer.fit_transform(bow_cu).toarray() """

    return bow_cu
    
def gen_loglikelihood(bow_cu, bow_train, bow_cu_size, threshold):
    loglikelihood.llr(bow_cu, bow_train)
