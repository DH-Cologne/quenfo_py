# ## Imports
from configuration.config_model import Configurations
from training.train_models import Model
from . import knn_predictor
from . import regex_predictor

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
        knn_predicted = knn_predictor.gen_classes(cu.featurevector, model.model_knn)

        # b. REGEX PREDICTION: predict classes with regex
        # hier dann auch den regex predictor reinmachen und dann direkt vergleichen!
        # paragraph vllt nochmal normalisieren? also lower case und non alpha raus?
        # hier übergeben wir am besten direkt die klasse RegexClassifier.get_pattern() irgendwie sowas
        # der resource path muss auch noch dafür in der config hinzugefügt und gecheckt werden
        regex_path = Configurations.get_regex_path()
        reg_predicted = regex_predictor.gen_classes(cu.paragraph)


        
        # Set class
        cu.set_classID(knn_predicted)
        print(cu, knn_predicted)
