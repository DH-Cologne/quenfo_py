from . import gen_knn

def start_knn(tfidf_train, all_classes):

    clf = gen_knn.initialize_knn(tfidf_train, all_classes)
   
    return clf