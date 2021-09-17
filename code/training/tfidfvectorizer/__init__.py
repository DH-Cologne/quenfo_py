""" Init-Script for tfidf-training."""

# ## Imports
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.feature_extraction.text import TfidfVectorizer
from . import gen_vectorizer
from typing import Union
from scipy.sparse import csr_matrix

# ## Function
def start_tfidf(all_features: list) -> Union[TfidfVectorizer, csr_matrix]:
    # Call tfidf-training function
    model, tfidf_train = gen_vectorizer.initialize_vectorizer(all_features)
    return model, tfidf_train