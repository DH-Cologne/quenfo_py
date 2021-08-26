# ## Imports
from scipy.sparse.csr import csr_matrix
from sklearn.neighbors import KNeighborsClassifier 

# Functions
def gen_classes(vectorized_cu: csr_matrix, clf: KNeighborsClassifier) -> int:
    """ Function to predict the class for a cu.
    
    Parameters
    ----------
    vectorized_cu: csr_matrix
        The transformed cu.

    clf: sklearn.neighbors.KNeighborsClassifier
        The saved model. Type: KNeighborsClassifier
        
    Returns
    -------
    predicted: int
        The predicted class. """

    # use given classifier to predict a class for the vectorized_cu
    predicted = clf.predict(vectorized_cu)
    # extract class number from array and clean it
    predicted = int(predicted[0].replace('\n', ''))

    return predicted