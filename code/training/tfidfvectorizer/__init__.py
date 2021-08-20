from orm_handling import models
from . import gen_vectorizer

all_features = list()
all_classes=list()

def start_tfidf(all_features):
    
    model, tfidf_train = gen_vectorizer.initialize_vectorizer(all_features)

    return model, tfidf_train