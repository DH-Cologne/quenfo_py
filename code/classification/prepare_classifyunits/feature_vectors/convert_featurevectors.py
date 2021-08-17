from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import numpy as np


fitter =''


def gen_tfidf_cu(fus, fitter):

    tfidf_cu = fitter.transform([" ".join(fus)])

    return tfidf_cu
