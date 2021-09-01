""" Script to train the tfidf-vectorizer. """

# ## Imports
from configuration.config_model import Configurations
from sklearn.feature_extraction.text import TfidfVectorizer
import training
from typing import Union
from scipy.sparse import csr_matrix

# ## Function
def initialize_vectorizer(all_features: list) -> Union[TfidfVectorizer, csr_matrix]:
    """ Method to train a tfidf-vectorizer with given traindata-features

    Parameters
    ----------
    all_features: list
        list of all features from traindata
    
    Returns
    -------
    vectorizer: sklearn.feature_extraction.text.TfidfVectorizer
        The saved model. Type: TfidfVectorizer
        
    tfidf_train: csr_matrix
        The transformed traindata. """

    # Get Configuration Settings for Tfidf-Vectorizer
    config = Configurations.get_tfidf_config()

    # Instantiate TfidfVectorizer obj with defined Configuration-Settings and fit all given features (as fus) from traindata
    vectorizer = TfidfVectorizer(lowercase=config['lowercase'], max_df=config['max_df'], \
        min_df=config['min_df'], sublinear_tf=config['sublinear_tf'], use_idf=config['use_idf']).fit(all_features)
    
    # Transform Traindata with fitted vectorizer to matrix
    tfidf_train = vectorizer.transform(all_features)

    # Save the model
    training.helper.save_model(vectorizer)

    # Return vectorizer and matrix
    return vectorizer, tfidf_train