

def gen_classes(tfidf_cu, clf):
    # prototyp prediction
    predicted = clf.predict(tfidf_cu)

    return predicted
    