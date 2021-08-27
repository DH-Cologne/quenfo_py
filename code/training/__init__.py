""" Script manages the training-process. The Class Model is filled with the knn classifier and the tfidf vectorizer."""

# ## Imports
from training import regexclassifier
from training.tfidfvectorizer import start_tfidf
from training.knnclassifier import start_knn
from classification import prepare_classifyunits
from orm_handling import orm
import logging
import sklearn
import dill as pickle
from pathlib import Path
from training.train_models import Model, SaveModel, TraindataInfo
from configuration.config_model import Configurations
from typing import Union
import inspect
import os
import datetime

# ## Set variables
all_features = list()
all_classes=list()
traindata_name = str()
traindata_date = str()
model = None

# ## Functions
def initialize_model() -> Model:
    """ Function to start the training/loading process of the Model. 
    a. try to load the models tfidf and knn (returns list of models in pickle file)
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
    global model
    
    """ STEP 1: TRY TO LOAD MODELS """    
    # Load tfidf-vectorizer and knn-model --> extract additional information about used traindata
    all_models_tfidf = load_model('model_tfidf')
    all_models_knn = load_model('model_knn')

    # Extract traindata name and last modification
    traindata_name, traindata_date = __get_traindata_information()

    """ STEP 2:  CHECK IF MODEL(S) WERE ALREADY TRAINED (separatly for tfidf and knn) """
    if all_models_tfidf is not None and all_models_knn is not None:
        # iterate over each model in pickle-file and check if one matches criteria
        for model_tfidf_obj, model_knn_obj in zip(all_models_tfidf, all_models_knn):
    
            # try to extract one specific model and the related traindata information from the model_obj
            try:
                model_tfidf = (model_tfidf_obj)[0].name     # vectorizer
                model_tfidf_td_info = (model_tfidf_obj)[1]  # traindata information for traindata used while fitting of vectorizer
                model_knn = (model_knn_obj)[0].name         # knn
                model_knn_td_info = (model_knn_obj)[1]      # traindata information for traindata used while fitting of knn
            except:
                # if errors occur, set all vars to None
                model_tfidf = model_knn = model_tfidf_td_info = model_knn_td_info = None


            # check if the current model matches all criteria (not None, same traindata input (name, date), same configurations, is fitted)
            if model_tfidf is not None and model_knn is not None \
                and model_tfidf_td_info.name == traindata_name  and model_knn_td_info.name == traindata_name \
                and model_tfidf_td_info.date == traindata_date and model_knn_td_info.date == traindata_date\
                and __check_configvalues(Configurations.get_tfidf_config(), model_tfidf) == True \
                and __check_configvalues(Configurations.get_knn_config(), model_knn) == True \
                and __check_fitted(model_tfidf, 'model_tfidf') and __check_fitted(model_knn, 'model_knn'):
                # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
                model = Model(model_knn, model_tfidf, traindata_name, traindata_date)
                break 

    """ STEP 3: TRAIN AGAIN IF MODEL IS STILL NOT FILLED (NO MATCHING MODEL FOUND OR PROBLEMS WHILE LOADING)"""
    if model == None:
   
        print('Model criteria didnt match. Both need to be redone')
        
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

        # STORING
        # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
        model = Model(model_knn, model_tfidf, traindata_name, traindata_date)

    # set regex classifier
    regex_clf = regexclassifier.call_regex_clf()
    model.set_regex_clf(regex_clf)

    # return obj of class Model
    return model



# ## (Private) Helper Functions

# Extract traindata name and last modification date
def __get_traindata_information() -> Union[str, str]:
    try:
        traindata_name = str(Path(Configurations.get_traindata_path()).name)
        traindata_date = str(datetime.datetime.fromtimestamp(os.path.getmtime(str(Configurations.get_traindata_path()))).replace(microsecond=0))
    except OSError:
        print("Key Information for Traindata could not be extracted. Model will be saved without Traindata Information.")
        traindata_name = traindata_date = str()
    return traindata_name, traindata_date

# Check if both configuration values are the same and return bool
def __check_configvalues(config_values: dict, model: Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> bool:
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

def save_model(model: Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]) -> None:
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

    def __dumper(model_path: Path, models_to_dump: list):
        with open(Path(model_path), 'wb') as fw:
            # Pack Model and Traindata Information in Objects to pickle dump them
            # Specific Filler-Classes are used (in models.py) just du store both informations in one pickle file.
            pickle.dump(models_to_dump, fw)
    
    # Check if Path already exists and append or overwrite old model
    if Path(model_path).exists():
        try:
            print(f'Model {model_path} does already exist, new model will be appended.')
            # load all already stored models from file
            old_models = __extract_models(model_path)
            # append stored models and new model --> dump them together in pickle file
            __dumper(model_path, old_models + [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])
        except:
            print(f'Problems while appending, model file will be overwritten with new model.')
            __dumper(model_path, [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])    
    else:
        __dumper(model_path, [[SaveModel(model),TraindataInfo(traindata_name, traindata_date)]])

# Methods to load the tfidf-models (are used by sanity, analysis inside and outside)
def load_model(name: str) -> Union[sklearn.feature_extraction.text.TfidfVectorizer or sklearn.neighbors.KNeighborsClassifier]: 
    """ Method loads a model depending on chosen name. Path for model is set in config.yaml
        1. __loader: loads the model 
            --> split loaded pickle obj into the model and the additonally stored trainingdata-information (extract_model)
        2. __check_fitted: checks the received model 

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
        all_models = __extract_models(Configurations.get_tfidf_path())
    elif name == 'model_knn':
        all_models = __extract_models(Configurations.get_knn_path())
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
    

def __check_fitted(model: Union[sklearn.feature_extraction.text.TfidfVectorizer, sklearn.neighbors.KNeighborsClassifier], name):
    try:
        # check if model is already fitted (example from https://www.py4u.net/discuss/230863)
        if (0 < len( [k for k,v in inspect.getmembers(model) if k.endswith('_') and not k.startswith('__')])) and model is not None:
            print(f'Model {name} is loaded and returned to next processing step.')
            return model
        else:
            raise TypeError
    except sklearn.exceptions.NotFittedError and TypeError:
        print(f'Model {name} failed to be loaded or is not fitted. Check Settings in config and paths for {name}. New Trainingprocess starts.')
        return model