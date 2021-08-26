""" Script manages the training-process. The Class Model is filled with the knn classifier and the tfidf vectorizer."""

# ## Imports
from training.tfidfvectorizer import start_tfidf
from training.knnclassifier import start_knn
from classification import prepare_classifyunits
from database import session, session2
from orm_handling import models, orm
import logging
import sklearn
import dill as pickle
from pathlib import Path
from orm_handling.models import Model, TraindataInfo, SaveModel, Configurations
from typing import Union
import inspect
import os
import datetime

# ## Set variables
all_features = list()
all_classes = list()
traindata_name = str()
traindata_date = str()


# ## Functions
def initialize_model() -> Model:
    """ Function to start the training/loading process of the Model. 
    a. try to load the models tfidf and knn
    b. check if models are already trained under same conditions and if the same traindata is used as before
    c. train again if loading fails or new configurations are set or new traindata is given
        
    Returns
    -------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information """

    # Set globals
    global all_features
    global all_classes
    global traindata_name
    global traindata_date

    # Load tfidf-vectorizer and knn-model --> extract additional information about used traindata
    model_tfidf, td_info_tfidf = load_model('model_tfidf')
    model_knn, td_info_knn = load_model('model_knn')

    # Extract traindata name and last modification
    traindata_name, traindata_date = __get_traindata_information()

    # CHECK IF NEW TRAINING IS NEEDED
    # Check if a. models are not None, b. same traindata was used (same file-name and same last modification date) and c. settings are the same
    if model_tfidf is None or model_knn is None \
            or td_info_tfidf.name != traindata_name or td_info_tfidf.date != traindata_date \
            or td_info_knn.name != traindata_name or td_info_knn.date != traindata_date \
            or __check_configvalues(Configurations.get_tfidf_config(), model_tfidf) == False \
            or __check_configvalues(Configurations.get_knn_config(), model_knn) == False:
        print('one of the models tfidf or knn was not filled. Both need to be redone')

        # PREPARATION
        # prepare data for training --> process data to fus
        traindata = __prepare_traindata()
        # make two lists from traindata --> one contains the features and one contains the classes
        all_features, all_classes = __prepare_lists(traindata)

        # TRAINING
        # Use all_features to fit a tfidf-vectorizer --> Return the vectorizer (model_tfidf) and the transformed traindata as matrix
        model_tfidf, tfidf_train = start_tfidf(all_features)
        # Use traindata matrix (tfidf_train) and list of depending classes to train a KNN-Classifier --> Returns KNN-Classifier
        model_knn = start_knn(tfidf_train, all_classes)

    # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
    model = Model(model_knn, model_tfidf, traindata_name, traindata_date)
    return model


# ## (Private) Helper Functions

# Extract traindata name and last modification date
def __get_traindata_information() -> Union[str, str]:
    try:
        traindata_name = str(Path(Configurations.get_traindata_path()).name)
        traindata_date = str(
            datetime.datetime.fromtimestamp(os.path.getmtime(str(Configurations.get_traindata_path()))).replace(
                microsecond=0))
    except OSError:
        print(
            "Key Information for Traindata could not be extracted. Model will be saved without Traindata Information.")
        traindata_name = traindata_date = str()
    return traindata_name, traindata_date


# Check if both configuration values are the same and return bool
def __check_configvalues(config_values: dict, model: Union[
    sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> bool:
    for i in (config_values).items():
        if i in model.get_params().items():
            config_bool = True
            pass
        else:
            config_bool = False
            break
    return config_bool


# Load traindata as orms and process them to fus
def __prepare_traindata() -> list:
    # Load the TrainingData: TrainingData in TrainingData Class
    traindata = orm.get_traindata()
    # fill classify_units and generate feature_units for Traindata
    for train_obj in traindata:
        prepare_classifyunits.generate_train_cus(train_obj)
    return traindata


# Help function to generate a list with all features and a list with all classes
# both lists are needed as input for training-process
def __prepare_lists(traindata: list) -> Union[list, list]:
    for train_obj in traindata:
        for cu in train_obj.children2:
            all_features.append(' '.join(cu.featureunits))
            all_classes.append(cu.classID)
    return all_features, all_classes


# ## Support Functions (Model related)
""" Methods to load and save models from all parts of the program."""


def save_model(model: Union[
    sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> None:
    """ Method saves a passed model in path (set in config).
        
    Parameters
    ----------
    model: sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier
        The model to be saved. Type: TfidfVectorizer or KNeighborsClassifier """

    # Set right path (from config.yaml) depending on type of model
    if type(model) == sklearn.feature_extraction.text.TfidfVectorizer:
        model_path = Configurations.get_tfidf_path()
    elif type(model) == sklearn.neighbors.KNeighborsClassifier:
        model_path = Configurations.get_knn_path()
    else:
        print(f'Path for {model} could not be resolved. No model was saved. Check config for path adjustment.')
        pass

    def __dumper(model_path: Path):
        with open(Path(model_path), 'wb') as fw:
            # Pack Model and Traindata Information in Objects to pickle dump them
            # Specific Filler-Classes are used (in models.py) just du store both informations in one pickle file.
            pickle.dump([SaveModel(model), TraindataInfo(traindata_name, traindata_date)], fw)

    # Check if Path already exists and overwrite old model
    if Path(model_path).exists():
        print(f'Model {model_path} does already exist, will be overwritten.')
        __dumper(model_path)
    else:
        __dumper(model_path)


# Methods to load the tfidf-models (are used by sanity, analysis inside and outside)
def load_model(name: str) -> Union[
    sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]:
    """ Method loads a model depending on chosen name. Path for model is set in config.yaml
        1. __loader: loads the model 
            --> split loaded pickle obj into the model and the additonally stored trainingdata-information (extract_model)
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
    model: sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier
        The saved model. Type: TfidfVectorizer or KNeighborsClassifier"""

    # Set model and traindata_information to None
    model = td_info = None
    # Load the Model and return it + the given traindata-information
    model, td_info = __loader(model, name)
    # Check if the model is already fitted. If it contains not fitting related information, set model to None
    model = __check_model(model, name)
    return model, td_info


def __loader(model: None, name: str):
    if name == 'model_tfidf':
        model, td_info = __extract_model(Configurations.get_tfidf_path())
    elif name == 'model_knn':
        model, td_info = __extract_model(Configurations.get_knn_path())
    else:
        model = td_info = None
    return model, td_info


def __extract_model(model_path):
    try:
        # load information stored in pickle file
        all_objs = pickle.load(open(Path(model_path), 'rb'))
        # split the pickle data into the model (comes first) and the traindata-information (stored at second place)
        model = (list(all_objs))[0].name
        td_info = (list(all_objs))[1]
    except FileNotFoundError:
        model = td_info = None
    return model, td_info


def __check_model(model: Union[sklearn.feature_extraction.text.TfidfVectorizer, sklearn.neighbors.KNeighborsClassifier],
                  name):
    try:
        # check if model is already fitted (example from https://www.py4u.net/discuss/230863)
        if (0 < len([k for k, v in inspect.getmembers(model) if
                     k.endswith('_') and not k.startswith('__')])) and model is not None:
            print(f'Model {name} is loaded and returned to next processing step.')
            return model
        else:
            raise TypeError
    except sklearn.exceptions.NotFittedError and TypeError:
        print(
            f'Model {name} failed to be loaded or is not fitted. Check Settings in config and paths for {name}. New Trainingprocess starts.')
        return model
