""" Script contains all training related Classes."""

# ## Imports
import sklearn

# class Model which contains the knnclassifier and the tfidfvectorizer
class Model():
    # Set knn
    model_knn = sklearn.neighbors.KNeighborsClassifier()
    # Set vectorizer
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    # Set traindata information
    traindata_name = str()
    traindata_date = str()
    # init-function to set values, works as constructor
    def __init__(self, model_knn, vectorizer, traindata_name, traindata_date):
        self.model_knn = model_knn
        self.vectorizer = vectorizer
        self.traindata_name = traindata_name
        self.traindata_date = traindata_date

# class just to dump the traindatainfo with model
class TraindataInfo():
    def __init__(self, name, date):
        self.name = name
        self.date = date
    # Setter
    def set_name(self, value):
        self.name = value
    def set_date(self, value):
        self.date = value

# class just to dump model 
class SaveModel:
    def __init__(self, name):
        self.name = name

    def set_name(self, value):
        self.name = value