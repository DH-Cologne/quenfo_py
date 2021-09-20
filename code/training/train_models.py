""" Script contains all training related Classes."""

# ## Imports
import sklearn
import pandas as pd

# Class Model contains the knnclassifier, tfidfvectorizer and regexclassifier
class Model():
    # Set Variables
    model_knn = sklearn.neighbors.KNeighborsClassifier()            # Set knn
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()  # Set vectorizer
    regex_clf = pd.DataFrame()                                      # Set regex_clf
    # Set traindata information
    traindata_name = str()
    traindata_date = str()

    # init-function to set values, works as constructor
    def __init__(self, model_knn, vectorizer, traindata_name, traindata_date):
        self.model_knn = model_knn
        self.vectorizer = vectorizer
        self.traindata_name = traindata_name
        self.traindata_date = traindata_date

    # Setter
    def set_regex_clf(self, value):
        self.regex_clf = value
    # Getter
    def get_regex_clf(self):
        return self.regex_clf

# DUMPING-Classes (only purpose)

# Class SaveModel to tump the Model
class SaveModel:
    def __init__(self, name):
        self.name = name

    def set_name(self, value):
        self.name = value

# Class TraindataInfo to dump the traindatainfo with model
class TraindataInfo():
    def __init__(self, name, date):
        self.name = name
        self.date = date
    # Setter
    def set_name(self, value):
        self.name = value
    def set_date(self, value):
        self.date = value