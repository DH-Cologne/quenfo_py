""" Script manages the prediction of classes via knn- and reg-classifier and comparing/merging of results. At the end a final class is set for cu. """

# ## Imports
from training.train_models import Model
from . import knn_predictor
from . import regex_predictor
from . import result_merger

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
        Class Model contains tfidf_vectorizer, knn_clf, regex_clf (further information about class in orm_handling/models.py)
        and traindata-information """

    # Iterate over each classifyunit
    for cu in jobad.children:
    
        # a. KNN PREDICTION: predict classes with knn
        knn_predicted = knn_predictor.gen_classes(cu.featurevector, model.model_knn)

        # b. REGEX PREDICTION: predict classes with regex
        reg_predicted = regex_predictor.gen_classes(cu.paragraph, model.get_regex_clf())

        # c. MERGE: compare the prediction from knn and regex
        if reg_predicted:                                                   # if regex pattern suggested a prediction
            predicted = result_merger.merge(reg_predicted, knn_predicted)   # compare knn and regex results
        else:                                                               # no regex class was predicted, use knn
            predicted = knn_predicted

        # Set class
        cu.set_classID(predicted)
