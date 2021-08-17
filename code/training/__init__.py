# ## Imports
from inspect import Attribute
from training.tfidfvectorizer import start_tfidf
from classification import prepare_classifyunits
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
from typing import Union
import inspect


# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    models = cfg['models']
    tfidf_path = models['tfidf_path']
    knn_path = models['knn_path']


# load traindata 
# check if tfidfmodel is already there and if it is filled with the same trainingdata and the same parameter
    #if true: load the vectorizer and transform traindata
        # output: fitter and tfidf_train matrix -- set all_classes and all_features
    # if false: use traindata to fit the model and transform traindata
        # output: fitter tfidf_trainmatrix -- set all_classes and all_features

all_features = list()
all_classes=list()

def initialize_model():
    global all_classes
    global all_features

    # Model besteht aus vectorizer und dem knn
    model_tfidf = load_model('model_tfidf')

    model_knn = load_model('model_knn')
    
    traindata = prepare_traindata()
    all_features, all_classes = __prepare_lists(traindata)

    tfidf_train = None

    # check if one of the models is None (not yet trained or loading failed) or if the models were already trained with the same trainingdata
    # TODO: irgendwo vllt auch in models oder in der config festlegen unter welchen parametern die modelle traineirt werden sollen (zum Abgleich)

    if model_tfidf is None or model_knn is None or model_tfidf.get_feature_names() != sorted(list(dict.fromkeys((" ".join(all_features)).split()))):
        print('one of the models tfidf or knn was not filled. Both need to be redone')
        
        model_tfidf, tfidf_train = start_tfidf(all_features)
        # hier wird knn trainiert mit tfidf_train und classes
        model_knn = start_knn(tfidf_train, all_classes)

    model = Model(model_knn=model_knn, vectorizer=model_tfidf)
    # bow traindata not needed --> hier an dieser stelle ist das knn auch schon vorhanden!

    return model

def __prepare_lists(traindata):
    for train_obj in traindata:
        for cu in train_obj.children2:
            all_features.append(' '.join(cu.featureunits))
            all_classes.append(cu.classID)
    return all_features, all_classes
    

def prepare_traindata():
    # ## STEP 2:
    # Load the TrainingData: TrainingData in TrainingData Class
    traindata = orm.get_traindata(session2)

    # fill classify_units (already there same as trainobjcontent) and genearte feature_units for Traindata
    for train_obj in traindata:
        prepare_classifyunits.generate_train_cus(train_obj)
        
    return traindata



# ## Support Functions
""" Methods to load and save models from all parts of the program."""

def save_model(model: Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> None:
    """ Method saves a passed model in path (set in config.yaml).
        
    Parameters
    ----------
    model: sklearn.feature_extraction.text.TfidfVectorizer
        The model to be saved. Type: TfidfVectorizer """
    
    model_path = None
    # set right path

    if type(model) == sklearn.feature_extraction.text.TfidfVectorizer:
        model_path = tfidf_path
    elif type(model) == sklearn.neighbors.KNeighborsClassifier:
        model_path = knn_path
    else:
        print(f'Path for {model} could not be resolved. No model was saved. Check config for path adjustment.')

    def __dumper(model: sklearn.feature_extraction.text.TfidfVectorizer, model_path: Path):
        with open(Path(model_path), 'wb') as fw:
            pickle.dump(model, fw)

    if Path(model_path).exists():
        print(f'Model {model_path} does already exist, will be overwritten.')
        __dumper(model, model_path)
    else:
        __dumper(model, model_path)

# Methods to load the tfidf-models (are used by sanity, analysis inside and outside)
def load_model(name: str) -> Union[sklearn.feature_extraction.text.TfidfVectorizer, sklearn.neighbors.KNeighborsClassifier]: 
    """ Method loads a model depending on chosen name. Path for model is set in config.yaml.
        1. __loader: loads the model and excepts Exceptions
        2. __check_model: checks the received model 
    Parameters
    ----------
    name : str
        Name of the model (model)
    
    Raises
    ------
    FileNotFoundError
        Raise Exception if model could not be loaded
    
    Returns
    -------
    model: sklearn.feature_extraction.text.TfidfVectorizer
        The saved model. Type: TfidfVectorizer """

    model = None

    def __loader(model: None, name: str):

        if name == 'model_tfidf':
            try:
                model = pickle.load(open(Path(tfidf_path), 'rb'))
            except FileNotFoundError as err:
                model = None
        elif name == 'model_knn':
            try:
                model = pickle.load(open(Path(knn_path), 'rb'))
            except FileNotFoundError as err:
                model = None
        else:
            model = None

        return model
    model = __loader(model, name)

    def __check_model(model: Union[sklearn.feature_extraction.text.TfidfVectorizer, sklearn.neighbors.KNeighborsClassifier], name):
        try:
            # check if model is already fitted (eg from https://www.py4u.net/discuss/230863)
            if (0 < len( [k for k,v in inspect.getmembers(model) if k.endswith('_') and not k.startswith('__')])) and model is not None:
                print(f'Model {name} is loaded and returned to next processing step.')
                return model
            else:
                raise TypeError
        except sklearn.exceptions.NotFittedError and TypeError:
            print(f'Model {name} failed to be loaded or is not fitted. Check Settings in config.yaml and paths for {name}. New Trainingprocess starts.')
            return model
    model = __check_model(model, name)

    return model