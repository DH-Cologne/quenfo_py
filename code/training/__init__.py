""" Script manages the training-process. The Class Model is filled with the knn classifier and the tfidf vectorizer."""

# ## Imports
from training.tfidfvectorizer import start_tfidf
from training.knnclassifier import start_knn
from classification import prepare_classifyunits
from database import session, session2
from orm_handling import models, orm
import logging
import sklearn
import pickle
import yaml
from pathlib import Path
from orm_handling.models import Model
from typing import Union
import inspect
import os
import datetime


# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    models = cfg['models']
    tfidf_path = models['tfidf_path']
    knn_path = models['knn_path']
    tfidf_config = cfg['tfidf_config']
    resources = cfg['resources']
    traindata_path = resources['traindata_path']

# ## Set variables
all_features = list()
all_classes=list()

# ## Functions
def initialize_model() -> Model:
    """ Function to start the training/loading process of the Model. 
    a. try to load the models tfidf and knn
    b. check if models are already trained with the same configurations
    c. train again if loading fails or new configurations are set
    """
    # load traindata 
    # check if tfidfmodel is already there and if it is filled with the same trainingdata and the same parameter
        #if true: load the vectorizer and transform traindata
            # output: fitter and tfidf_train matrix -- set all_classes and all_features
        # if false: use traindata to fit the model and transform traindata
            # output: fitter tfidf_trainmatrix -- set all_classes and all_features

    # set variables global
    global all_classes
    global all_features

    # Model besteht aus vectorizer und dem knn
    model_tfidf = load_model('model_tfidf')

    model_knn = load_model('model_knn')
    
    # extract traindata name and last modification
    try:
        traindata_namedate = ('').join([str(Path(traindata_path).name), '$', str(datetime.datetime.fromtimestamp(os.path.getmtime(traindata_path)).replace(microsecond=0))])
    except OSError:
        print("Key Information for Traindata could not be extracted. Model will be saved without Traindata Information.")
        traindata_namedate = ''

    if model_tfidf is None or model_knn is None \
        or model_tfidf.input != traindata_namedate \
        or model_knn.input != traindata_namedate: # check if inputname in model_tfidf is not the same as traindata_namedate: means, the traindata is new or modified.
        print('one of the models tfidf or knn was not filled. Both need to be redone')
        
        traindata = prepare_traindata()
        all_features, all_classes = __prepare_lists(traindata)

        tfidf_train = None

        model_tfidf, tfidf_train = start_tfidf(all_features, traindata_namedate)
        # hier wird knn trainiert mit tfidf_train und classes
        model_knn = start_knn(tfidf_train, all_classes, traindata_namedate)

    model = Model(model_knn=model_knn, vectorizer=model_tfidf)
    # bow traindata not needed --> hier an dieser stelle ist das knn auch schon vorhanden!

    return model

#  Help function to generate a list with all features and a list with all classes
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