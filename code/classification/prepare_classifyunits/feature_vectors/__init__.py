# ## Imports
from training.train_models import Model
from . import convert_featurevectors

# ## Function
def get_featurevectors(cu: object, model: Model) -> None:
    """ Function to vectorize the fus of a classifyunit.

    Parameters
    ----------
    cu: object
        object of Class ClassifyUnits: contains content and featureunits
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # Pass fus and vectorizer to vectorization
    vectorized_cu = convert_featurevectors.gen_tfidf_cu(cu.featureunits, model.vectorizer)

    # Set returned vector 
    cu.set_featurevector(vectorized_cu)
