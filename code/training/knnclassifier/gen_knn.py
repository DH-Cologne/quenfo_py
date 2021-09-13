""" Script contains the training of the knn_classifier. """
# ## Imports
from scipy.sparse.csr import csr_matrix
from configuration.config_model import Configurations
from sklearn.neighbors import KNeighborsClassifier 
import training 
import configuration

# ## Function
def initialize_knn(vectorized_train: csr_matrix, all_classes: list) -> KNeighborsClassifier:
     """ Method to train a knn-classifier with given traindata matrix and classes

     Parameters
     ----------
     vectorized_train: csr_matrix
        The transformed traindata.

     all_classes: list
          list of all classes from traindata
     
     Returns
     -------
     clf: sklearn.neighbors.KNeighborsClassifier
        The saved model. Type: KNeighborsClassifier """

     # Get Configuration Settings for KNN-Classifier
     config = configuration.config_obj.get_knn_config()

     # Instantiate KNNClassifier obj with defined Configuration-Settings
     knn = KNeighborsClassifier(n_neighbors=config['n_neighbors'], weights=config['weights'], \
          algorithm=config['algorithm'], leaf_size=config['leaf_size'])

     # Fit the knn with the given traindata-matrix and related classes
     clf = knn.fit(vectorized_train, all_classes)

     # save the model
     training.helper.save_model(clf)

     # return classifier
     return clf