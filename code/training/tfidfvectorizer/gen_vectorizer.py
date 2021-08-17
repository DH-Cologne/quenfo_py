from orm_handling.models import Model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

import training

tfidf_train = ''
vectorizer =''


def initialize_vectorizer(all_features):

    global tfidf_train
    global vectorizer
    
    vectorizer = TfidfVectorizer(lowercase=False).fit(all_features)
    tfidf_train = vectorizer.transform(all_features)

    # save the model
    training.save_model(vectorizer)


    return vectorizer, tfidf_train

    


