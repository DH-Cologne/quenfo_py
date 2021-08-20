from orm_handling import models
from . import gen_vectorizer

all_features = list()
all_classes=list()

def start_tfidf(all_features, config):
    
    model, tfidf_train = gen_vectorizer.initialize_vectorizer(all_features, config)

    return model, tfidf_train