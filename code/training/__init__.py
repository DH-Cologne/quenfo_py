""" Script manages the training-process. The Class Model is filled with the knn classifier, the tfidf vectorizer and regex classifier."""

# ## Imports
from training import regexclassifier
from training.tfidfvectorizer import start_tfidf
from training.knnclassifier import start_knn
from training.train_models import Model
from training import helper
import configuration
import logging

# ## Set variables
model = None

# ## Functions
def initialize_model() -> Model:
    """ Function to start the training/loading process of the Model. 
    a. try to load the models tfidf and knn (returns list of models in pickle file)
    b. check if models are already trained under same conditions and if the same traindata is used as before
    c. train again if loading fails or new configurations are set or new traindata is given
    d. load and set regex classifier
        
    Returns
    -------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py), 
        traindata-information and regex_classifier """
    
    # Set globals
    global model
    
    """ STEP 1: TRY TO LOAD MODELS AND TRAINDATA INFORMATION """  
    # Load tfidf-vectorizer and knn-model --> extract additional information about used traindata
    all_models_tfidf = helper.load_model('model_tfidf')
    all_models_knn = helper.load_model('model_knn')

    # Extract traindata name and last modification
    traindata_name, traindata_date = helper.get_traindata_information()

    """ STEP 2:  CHECK IF MODELS ARE ALREADY TRAINED (separatly for tfidf and knn) """
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
                and helper.check_configvalues(configuration.config_obj.get_tfidf_config(), model_tfidf) == True \
                and helper.check_configvalues(configuration.config_obj.get_knn_config(), model_knn) == True \
                and helper.check_fitted(model_tfidf, 'model_tfidf') and helper.check_fitted(model_knn, 'model_knn'):
                
                # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
                model = Model(model_knn, model_tfidf, traindata_name, traindata_date)
                break 

    """ STEP 3: TRAIN AGAIN IF MODEL IS STILL NOT FILLED (NO MATCHING MODEL FOUND OR PROBLEMS WHILE LOADING)"""
    if model == None:
   
        print('Model criteria didnt match. Both need to be redone')
        logging.info('Model criteria didnt match. Both need to be redone')
        
        # PREPARATION
        # prepare data for training --> process data to fus
        traindata = helper.prepare_traindata()
        # make two lists from traindata --> one contains the features and one contains the classes
        all_features, all_classes = helper.prepare_lists(traindata)

        # TRAINING
        # Use all_features to fit a tfidf-vectorizer --> Return the vectorizer (model_tfidf) and the transformed traindata as matrix
        model_tfidf, tfidf_train = start_tfidf(all_features)
        # Use traindata matrix (tfidf_train) and list of depending classes to train a KNN-Classifier --> Returns KNN-Classifier
        model_knn = start_knn(tfidf_train, all_classes)

        # STORING
        # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
        model = Model(model_knn, model_tfidf, traindata_name, traindata_date)

    """ STEP 4: LOAD AND SET REGEX CLASSIFIER """
    # set regex classifier
    regex_clf = regexclassifier.call_regex_clf()
    model.set_regex_clf(regex_clf)

    # TODO: Letzter Checkup, ob auch jetzt alles gefüllt ist. 

    # return obj of class Model
    return model