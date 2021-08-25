# ## Imports
import sys
from scipy.sparse.csr import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

# ## Set Variables
vectorizer= str()

# ## Function
def gen_tfidf_cu(fus: list, vectorizer: TfidfVectorizer) -> csr_matrix:  
    """ Function to vectorize the fus of a classifyunit.

    Parameters
    ----------
    fus: list
        list of featureunits of one cu
    vectorizer: TfidfVectorizer
        vectorizer object contains the fitted vocab of Trainingdata
    
    Raises
    ------
    AttributeError
        If vectorizer is empty, AttributeError is raised 
        
    Returns
    -------
    vectorized_cu: csr_matrix
        transformed classifyunit """

    try:
        # transform fus from cu
        vectorized_cu = vectorizer.transform([" ".join(fus)])
        return vectorized_cu
    except AttributeError:
        print(f'Error: Vectorizer is empty or not working. Check tfidf_model and start again.')
        sys.exit()