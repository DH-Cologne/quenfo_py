# ## Imports
from orm_handling.models import Model
from . import knn_predictor

# ## Functions
def start_prediction(jobad: object, model: Model) -> None:
    """ Function manages the prediction of the classes for each cu.
        a. use the knn to predict classes
        b. use regex to predict classes
        c. compare both predictions and merge them together

    Parameters
    ----------
    jobad: object
        jobad is an object of the class JobAds and contains all given variables 
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # Iterate over each classifyunit
    for cu in jobad.children:

        # a. KNN PREDICTION: predict classes with knn
        predicted = knn_predictor.gen_classes(cu.featurevector, model.model_knn)

        # b. REGEX PREDICTION: predict classes with regex
        # hier dann auch den regex predictor reinmachen und dann direkt vergleichen!
        
        # Set class
        cu.set_classID(predicted)
        # print(cu, predicted)
