""" Script contains all helper functions and support funcitons needed for modeling. The helper functions are mostly for handling and preparing the 
    traindata. The support functions are for handling the loading, checking and saving the models. """

# ## Imports
from typing import Union
import sklearn
import dill as pickle
from pathlib import Path
from training.train_models import SaveModel, TraindataInfo
import inspect
import os
import datetime
import classification
from orm_handling import orm
import configuration 
import logger

# ## Set variables
all_features = list()
all_classes = list()
traindata_name = str()
traindata_date = str()

# ## Helper Functions

# Extract traindata name and last modification date
def get_traindata_information() -> Union[str, str]:
    """ Method uses the traindata file to extract the name of the file and the last modification date.
    
    Raises
    ------
    OSError
        Raise Exception if Traindata Information failed to be extracted.
    
    Returns
    -------
    traindata_name: str
        Name of the traindata file.
    traindata_date: str
        Last modification date. """

    # Set globals
    global traindata_name
    global traindata_date
    try:
        traindata_name = str(Path(configuration.config_obj.get_traindata_path()).name)
        traindata_date = str(datetime.datetime.fromtimestamp(os.path.getmtime(str(configuration.config_obj.get_traindata_path()))).replace(microsecond=0))
    except OSError:
        logger.log_clf.warning("Key Information for Traindata could not be extracted. Model will be saved without Traindata Information.")
        print("Key Information for Traindata could not be extracted. Model will be saved without Traindata Information.")
        traindata_name = traindata_date = str()
    return traindata_name, traindata_date

# Check if both configuration values are the same and return bool
def check_configvalues(config_values: dict, model: Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> bool:
    """ Function compare configuration values and return bool.

    Parameters
    ----------
    config_values: dict
        configuration values set in configuration file

    model: TfidfVectorizer or KNeighborsClassifier
        model contains the settings used for training (model.get_params())
        
    Returns
    -------
    config_bool: bool
        "True" if settings are the same, "False" if they differentiate. """

    for i in (config_values).items():
        if i in model.get_params().items():
            config_bool = True
            pass
        else:
            config_bool = False
            break
    return config_bool

# Load traindata as orms and process them to fus
def prepare_traindata() -> list:
    """ Function to load the traindata and preprocess them to feature_units. 
    
    Returns
    -------
    traindata: list
        list of traindata objects """

    # Load the TrainingData: TrainingData in TrainingData Class
    traindata = orm.get_traindata()
    # fill classify_units and generate feature_units for Traindata
    for train_obj in traindata:
        classification.prepare_classifyunits.generate_train_cus(train_obj)  
    return traindata

# Help function to generate a list with all features and a list with all classes
# both lists are needed as input for training-process
def prepare_lists(traindata: list) -> Union[list, list]:
    """ Function to generate list with all featuers and a list with all classes 
    
    Parameters
    ----------
    traindata: list
        list of traindata objects 
        
    Returns
    -------
    all_features: list
        list of all features represented in traindata
    all_classes: list 
        list of all classes represented in traindata """
        
    # Set globals
    global all_features
    global all_classes
    for train_obj in traindata:
        for cu in train_obj.children2:
            all_features.append(' '.join(cu.featureunits))
            all_classes.append(cu.classID)
    return all_features, all_classes

# ## Support Functions (Model related)
""" Methods to load and save models from all parts of the program."""

def save_model(model: Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> None:
    """ Method saves a passed model in path (set in config).
        
    Parameters
    ----------
    model: sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier
        The model to be saved. Type: TfidfVectorizer or KNeighborsClassifier """

    # Set right path (from config.yaml) depending on type of model
    if type(model) == sklearn.feature_extraction.text.TfidfVectorizer:
        model_path = configuration.config_obj.get_tfidf_path()
    elif type(model) == sklearn.neighbors.KNeighborsClassifier:
        model_path = configuration.config_obj.get_knn_path()
    else:
        print(f'Path for {model} could not be resolved. No model was saved. Check config for path adjustment.')
        logger.log_clf.warning(f'Path for {model} could not be resolved. No model was saved. Check config for path adjustment.')
        pass

    def __dumper(model_path: Path, models_to_dump: list):
        with open(Path(model_path), 'wb') as fw:
            # Pack Model and Traindata Information in Objects to pickle dump them
            # Specific Filler-Classes are used (in models.py) just du store both informations in one pickle file.
            pickle.dump(models_to_dump, fw)
    
    # Check if Path already exists and append or overwrite old model
    if Path(model_path).exists():
        try:
            logger.log_clf.info(f'File {model_path} does already exist, new model will be appended.')
            # load all already stored models from file
            old_models = __extract_models(model_path)
            # append stored models and new model --> dump them together in pickle file
            __dumper(model_path, old_models + [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])
        except:
            logger.log_clf.warning(f'Problems while appending, model file will be overwritten with new model.')
            __dumper(model_path, [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])    
    else:
        __dumper(model_path, [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])

# Methods to load the tfidf-models (are used by sanity, analysis inside and outside)
def load_model(name: str) -> Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]: 
    """ Method loads a model depending on chosen name. Path for model is set in config.yaml
        1. __loader: loads the model 
            --> split loaded pickle obj into the model and the additonally stored trainingdata-information (extract_model)

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
    all_models: list
        list contains all models for TfidfVectorizer or KNeighborsClassifier and traindata information"""

    # Set all_models to None
    all_models = None
    # Load all models from the pickle file as list
    all_models = __loader(all_models, name)
    return all_models

def __loader(all_models: None, name: str):
    if name == 'model_tfidf':
        all_models = __extract_models(configuration.config_obj.get_tfidf_path())
    elif name == 'model_knn':
        all_models = __extract_models(configuration.config_obj.get_knn_path())
    else:
        all_models = None
    return all_models

def __extract_models(model_path: str) -> Union[list or None]:
    try:
        # load information stored in pickle file
        all_models = pickle.load(open(Path(model_path), 'rb')) 
    except (AttributeError, pickle.UnpicklingError, FileNotFoundError):
        all_models = None
    return all_models
    

def check_fitted(model: Union[sklearn.feature_extraction.text.TfidfVectorizer, sklearn.neighbors.KNeighborsClassifier], name):
    try:
        # check if model is already fitted (example from https://www.py4u.net/discuss/230863)
        if (0 < len( [k for k,v in inspect.getmembers(model) if k.endswith('_') and not k.startswith('__')])) and model is not None:
            print(f'Model {name} is loaded and returned to next processing step.')
            logger.log_clf.info(f'Model {name} is loaded and returned to next processing step.')
            return model
        else:
            raise TypeError
    except sklearn.exceptions.NotFittedError and TypeError:
        print(f'Model {name} failed to be loaded or is not fitted. Check Settings in config and paths for {name}. New Trainingprocess starts.')
        logger.log_clf.warning(f'Model {name} failed to be loaded or is not fitted. Check Settings in config and paths for {name}. New Trainingprocess starts.')
        return model