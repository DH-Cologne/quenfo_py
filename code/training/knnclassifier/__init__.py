from sklearn.neighbors import KNeighborsClassifier    

def start_knn(tfidf_train, all_classes):
    # knn prototyp
    knn = KNeighborsClassifier(n_neighbors=5)
    clf = knn.fit(tfidf_train, all_classes)

    return clf