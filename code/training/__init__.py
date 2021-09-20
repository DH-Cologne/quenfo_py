""" Script manages the training-process. The Class Model is filled with the knn classifier, the tfidf vectorizer and regex classifier."""

# ## Imports
from training import regexclassifier
from training.tfidfvectorizer import start_tfidf
from training.knnclassifier import start_knn
from training.train_models import Model
from training import helper
import configuration
import logger
import sys

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
    
    # Start
    print(f'\n\nTraining-Module started.')
    logger.log_clf.info(f'\n\nTraining-Module started.')

    # STEP 1: 
    __preparation()             # TRY TO LOAD MODELS AND TRAINDATA INFORMATION
    # STEP 2: 
    __check_and_fill_model()    # CHECK IF MODELS ARE ALREADY TRAINED (separatly for tfidf and knn)
    # STEP 3: 
    __train_model()             # TRAIN AGAIN IF MODEL IS STILL NOT FILLED (NO MATCHING MODEL FOUND OR PROBLEMS WHILE LOADING)
    # STEP 4:
    __load_regex()              # LOAD AND SET REGEX CLASSIFIER

    # Last check if Model is filled with Knn-clf, tfidf-vectorizer and regex-clf.
    __document_result()

    # End
    logger.log_clf.info(f'\nTraining-Module finished. Return to classification with filled Model.\n')
    print((f'Training-Module finished. Return to classification with filled Model.\n'))
    # return obj of class Model
    return model


""" STEP 1: TRY TO LOAD MODELS AND TRAINDATA INFORMATION """ 
def __preparation(): 
    # Set global
    global all_models_knn, all_models_tfidf, traindata_name, traindata_date

    # Load tfidf-vectorizer and knn-model --> extract additional information about used traindata
    all_models_tfidf = helper.load_model('model_tfidf')
    all_models_knn = helper.load_model('model_knn')

    # Extract traindata name and last modification
    traindata_name, traindata_date = helper.get_traindata_information()
    logger.log_clf.info(f'Traindata checkup: Traindata_name is {traindata_name} and Traindata_date is {traindata_date}')


""" STEP 2:  CHECK IF MODELS ARE ALREADY TRAINED (separatly for tfidf and knn) """
def __check_and_fill_model():
    global model
    if all_models_tfidf is not None and all_models_knn is not None:
        logger.log_clf.info(f'Models exist. Check if stored models have used same Traindata, \
            check if configuration settings in config.yaml and model are equal, \
                check if models are fitted.')
        # iterate over each model in pickle-file and check if one matches criteria
        for model_tfidf_obj, model_knn_obj in zip(all_models_tfidf, all_models_knn):
    
            # try to extract one specific model and the related traindata information from the model_obj
            try:
                model_tfidf = (model_tfidf_obj)[0].name     # vectorizer
                model_tfidf_td_info = (model_tfidf_obj)[1]  # traindata information for traindata used while fitting of vectorizer
                model_knn = (model_knn_obj)[0].name         # knn
                model_knn_td_info = (model_knn_obj)[1]      # traindata information for traindata used while fitting of knn
            except Exception:
                # if errors occur, set all vars to None
                model_tfidf = model_knn = model_tfidf_td_info = model_knn_td_info = None

            # check if the current model matches all criteria (not None, same traindata input (name, date), same configurations, is fitted)
            if model_tfidf is not None and model_knn is not None \
                and model_tfidf_td_info.name == traindata_name  and model_knn_td_info.name == traindata_name \
                and model_tfidf_td_info.date == traindata_date and model_knn_td_info.date == traindata_date\
                and helper.check_configvalues(configuration.config_obj.get_tfidf_config(), model_tfidf) == True \
                and helper.check_configvalues(configuration.config_obj.get_knn_config(), model_knn) == True \
                and helper.check_fitted(model_tfidf, 'model_tfidf') and helper.check_fitted(model_knn, 'model_knn'):

                logger.log_clf.info(f'Matching Model was found. Configurations: TFIDF -> {configuration.config_obj.get_tfidf_config()} \
                    KNN -> {configuration.config_obj.get_knn_config()}. Traindata: {helper.get_traindata_information()}')

                # Instantiate an object of class Model and store the tfidf-vectorizer, knn-classifier and the used traindata-information
                model = Model(model_knn, model_tfidf, traindata_name, traindata_date)
                break 

""" STEP 3: TRAIN AGAIN IF MODEL IS STILL NOT FILLED (NO MATCHING MODEL FOUND OR PROBLEMS WHILE LOADING)"""
def __train_model():
    global model
    if model == None:

        print('No matching KNN and/or Tfidf Model found. Both need to be redone.')
        logger.log_clf.info('No matching KNN and/or Tfidf Model found. Both need to be redone.')
        
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
def __load_regex():
    # set regex classifier
    regex_clf = regexclassifier.call_regex_clf()
    model.set_regex_clf(regex_clf)


""" LOG/PRINT Valid Model"""
def __document_result():
    if not(model.get_regex_clf().empty) and model.model_knn and model.vectorizer:
        logger.log_clf.info(f'Model is fully filled (KNN, TFIDF and REGEX) and can be used to classify data.')
        print(f'Model is fully filled (KNN, TFIDF and REGEX) and can be used to classify data.')
    elif model.model_knn and model.vectorizer:
        logger.log_clf.warning(f'Model is filled with knn-clf and vectorizer. Continue without regex-clf.')
        print(f'Model is filled with knn-clf and vectorizer. Continue without regex-clf.')
    else:
        logger.log_clf.warning(f'Error occurred while building/filling Model.')
        logger.log_clf.warning(f'Model Knn: {(model.model_knn)} and Model Tfidf: {(model.vectorizer)}')
        print(f'Error occurred while building/filling Model. Check logger-files.')
        sys.exit()