from sklearn.neighbors import KNeighborsClassifier 
import training 

def initialize_knn(tfidf_train, all_classes, traindata_namedate):
     # knn prototyp
    knn = KNeighborsClassifier(n_neighbors=5, input=traindata_namedate)
    clf = knn.fit(tfidf_train, all_classes)

    # save the model
    training.save_model(clf)
    return clf