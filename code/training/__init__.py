# ## Imports
from training.tfidfvectorizer import start_training
from classification.prepare_classifyunits import  generate_train_cus
from database import session, session2
from orm_handling import models, orm
import logging
import sys
from sklearn.utils.validation import check_is_fitted
import sklearn
import pickle
import yaml
from pathlib import Path
from orm_handling.models import Model
from training.knnclassifier import start_knn

# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    models = cfg['models']
    tfidf_path = models['tfidf_path']


# load traindata 
# check if tfidfmodel is already there and if it is filled with the same trainingdata and the same parameter
    #if true: load the vectorizer and transform traindata
        # output: fitter and tfidf_train matrix -- set all_classes and all_features
    # if false: use traindata to fit the model and transform traindata
        # output: fitter tfidf_trainmatrix -- set all_classes and all_features

all_features = list()
all_classes=list()

def initialize_model():

    model_tfidf = load_model('model_tfidf')

    # TODO: load knn
    model_knn = None

    # Zeile tiefer!! in erste if is none
    traindata = prepare_traindata()
    
    tfidf_train = ''
    # TODO: check if vocab was already trained
    #or model_tfidf.get_feature_names() == traindata
    if model_tfidf is None or model_knn is None:
        global all_classes
        global all_features

        def prepare_lists():
            for train_obj in traindata:
                for cu in train_obj.children2:
                    all_features.append(' '.join(cu.featureunits))
                    all_classes.append(cu.classID)
        prepare_lists()

        model_tfidf, tfidf_train = start_training(all_features)
        # hier wird knn trainiert mit tfidf_train und classes
        model_knn = start_knn(tfidf_train, all_classes)

    model = Model(model_knn=model_knn, vectorizer=model_tfidf)
    # bow traindata not needed --> hier an dieser stelle ist das knn auch schon vorhanden!

    return model



def prepare_traindata():
    # ## STEP 2:
    # Load the TrainingData: TrainingData in TrainingData Class
    traindata = orm.get_traindata(session2)

    # generate classify_units and feature_units for Traindata
    for train_obj in traindata:
        generate_train_cus(train_obj)
        
    return traindata



# ## Support Functions
""" Methods to load and save models from all parts of the program."""

def save_model(tfidf_model: sklearn.feature_extraction.text.TfidfVectorizer) -> None:
    """ Method saves a passed model in path (set in config.yaml).
        
    Parameters
    ----------
    model: sklearn.feature_extraction.text.TfidfVectorizer
        The model to be saved. Type: TfidfVectorizer """
    
    def __dumper(tfidf_model: sklearn.feature_extraction.text.TfidfVectorizer, tfidf_path: Path):
        with open(Path(tfidf_path), 'wb') as fw:
            pickle.dump(tfidf_model, fw)

    if Path(tfidf_path).exists():
        logging.warning(f'Model {tfidf_path} does already exist, will be overwritten.')
        __dumper(tfidf_model, tfidf_path)
    else:
        __dumper(tfidf_model, tfidf_path)

# Methods to load the tfidf-models (are used by sanity, analysis inside and outside)
def load_model(name: str) -> sklearn.feature_extraction.text.TfidfVectorizer:
    """ Method loads a model depending on chosen name. Path for model is set in config.yaml.
        1. __loader: loads the model and excepts Exceptions
        2. __check_model: checks the received model 
    Parameters
    ----------
    name : str
        Name of the model (tfidf_model)
    
    Raises
    ------
    FileNotFoundError
        Raise Exception if model could not be loaded
    
    Returns
    -------
    model: sklearn.feature_extraction.text.TfidfVectorizer
        The saved model. Type: TfidfVectorizer """

    tfidf_model = None

    def __loader(tfidf_model: None, name: str):
        try:
            if name == 'model_tfidf':
                tfidf_model = pickle.load(open(Path(tfidf_path), 'rb'))
        except FileNotFoundError:
            tfidf_model = None
        return tfidf_model
    tfidf_model = __loader(tfidf_model, name)

    def __check_model(tfidf_model: sklearn.feature_extraction.text.TfidfVectorizer):
        try:
            check_is_fitted(tfidf_model, '_tfidf', 'The tfidf vector is not fitted')
            print(f'Model {name} is loaded and returned to next processing step.')
            return tfidf_model
        except sklearn.exceptions.NotFittedError and TypeError:
            print(f'Model {name} failed to be loaded. Check Settings in config.yaml and paths {tfidf_path}. New Trainingprocess starts.')
            return tfidf_model

    tfidf_model = __check_model(tfidf_model)
    return tfidf_model