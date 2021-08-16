from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import numpy as np
from scipy.stats import norm

import loglikelihood
is_created = None
bow_train = ''
clf = ''
""" df = pd.DataFrame() """
fitter =''
all_features = list()
all_classes=list()
my_dict = list()
""" all_featuresagain = list() """

def initialize_bow_train(traindata, fus):
    """ global df
    global all_featuresagain """
    global is_created
    global bow_train
    global clf
    global fitter
    global all_classes
    global all_features
    global my_dict

    if is_created is None:
        for train_obj in traindata:
            for cu in train_obj.children2:
    
                #df = df.append([{'id':cu.id, 'classID': cu.classID, 'parent': cu.parent2, 'fus': cu.featureunits}], ignore_index=True)
                all_features.append(cu.featureunits)
                all_classes.append(cu.classID)

        fitter = TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit(all_features)
        bow_train = fitter.transform(all_features)

        # knn prototyp
        knn = KNeighborsClassifier(n_neighbors=5)
        clf = knn.fit(bow_train, all_classes)
        
        is_created = 'checked' 
        return bow_train, fitter, clf, all_classes
    else:
        return bow_train, fitter, clf, all_classes
    
    """ if is_created is None:
        for train_obj in traindata:
            for cu in train_obj.children2:
                cu_dict = dict()
                #df = df.append([{'id':cu.id, 'classID': cu.classID, 'parent': cu.parent2, 'fus': cu.featureunits}], ignore_index=True)
                all_features.append(cu.featureunits)
                all_classes.append(cu.classID)

                for fu in cu.featureunits:
                    #print(my_dict.keys())
                    if fu in cu_dict.keys(): 
                        cu_dict[fu] += 1  
                    else:
                        cu_dict[fu] = 1
                my_dict.append(cu_dict)
        print(my_dict)

        #print(all_features)
        

        fitter = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit(all_features)
        bow_train = fitter.transform(all_features).toarray()
        #print(bow_train)

        fitter = TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit(all_features)
        bow_train = fitter.transform(all_features)

        # knn prototyp
        knn = KNeighborsClassifier(n_neighbors=5)
        
        clf = knn.fit(bow_train, all_classes)
        
        is_created = 'checked' 
        return bow_train, fitter
    else:
        return bow_train, fitter """


def gen_bow_cu(fus, fitter):

    # nur die folgende Zeile hier, dann läuft mit tfidf
    bow_cu = fitter.transform([fus]).toarray()

    #bow_cu = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform([fus])

    #print(bow_cu)

    #bow_cu = loglikelihood.llr(np.matrix(bow_cu))


    #data = [1,2,3,4,5]
    #print(bow_cu)
    """ bow_cu = bow_cu.toarray()
    print(bow_cu)
    m,s = norm.fit([bow_cu])
    print(m, s)
    #log_likelihood = np.log(np.product(norm.pdf(bow_cu,m,s)))
    log_likelihood = np.sum(np.log(norm.pdf([bow_cu],m,s)))
    print("BREAK")
    print(log_likelihood) """

    """ tfidf_transformer = TfidfTransformer()
    bow_cu = tfidf_transformer.fit_transform(bow_cu).toarray() """

    return bow_cu
