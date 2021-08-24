# ## Imports
from scipy.sparse.csr import csr_matrix
from orm_handling.models import Configurations
from sklearn.neighbors import KNeighborsClassifier 
import training 

# ## Function
def initialize_knn(tfidf_train: csr_matrix, all_classes: list) -> KNeighborsClassifier:
     """ Method to train a knn-classifier with given traindata matrix and classes

     Parameters
     ----------
     tfidf_train: csr_matrix
        The transformed traindata.

     all_classes: list
          list of all classes from traindata
     
     Returns
     -------
     clf: sklearn.neighbors.KNeighborsClassifier
        The saved model. Type: KNeighborsClassifier """

     # Get Configuration Settings for KNN-Classifier
     config = Configurations.get_knn_config()

     # Instantiate KNNClassifier obj with defined Configuration-Settings
     knn = KNeighborsClassifier(n_neighbors=config['n_neighbors'], weights=config['weights'], \
          algorithm=config['algorithm'], leaf_size=config['leaf_size'])

     # Fit the knn with the given traindata-matrix and related classes
     clf = knn.fit(tfidf_train, all_classes)

     # save the model
     training.save_model(clf)

     # return classifier
     return clf