""" Main Script of the application. Manages the main components of the tool. """

# ## Imports
import configuration
import logging
from pathlib import Path
from timeit import default_timer as timer
from datetime import timedelta
import argparse
import sys
import os
import training
import classification
import database

# ## Initiate Logging-Module for Classification
logging.basicConfig(
    format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s',
    level=logging.DEBUG, filename=Path('logging/logger_classification.log'), filemode='w+',
)


def start_classification():
    
    # STEP 1: Train or Load Vectorizer, KNN and Regex_clf as Class-object model
    model = training.initialize_model()

    # STEP 2: Start Classification
    classification.classify(model)

def start_extraction():
    # STEP 3a: Information Extraction 
    pass

def start_matching():
    # STEP 3b: Matching 
    pass


def manage_app(args):
    method_args = vars(args)
    def __set_all():
        """ Set globals: configuration values and database connections. """
        configuration.set_config(method_args)
        database.set_train_conn()
        database.set_input_conn()
    __set_all()

    def __call_parts():
        # Call each part of the application (depending on given argparse arguments)
        if method_args['classification']:
            print(f'Classification started.')
            start_classification()
        if method_args['extraction']:
            print(f'Information Extraction started.')
            start_extraction()
        if method_args['matching']:
            print(f'Matching started.')
            start_matching()
        if  not(method_args['classification']) and not(method_args['extraction']) and not(method_args['matching']):
            print('All in one')
            print(f'Classification started.')
            start_classification()
            print(f'Information Extraction started.')
            start_extraction()
            print(f'Matching started.')
            start_matching()
    __call_parts()


# ArgumentParser für step modeling + classify, information extraction, matching

def get_application_parser() -> argparse.ArgumentParser:
    """ Function to generate an ArgumentParser and return given arguments from CLI
    Returns
    ----------
    application_parser : parser
        Parser contains the subparsers: id_handling, modeling, analysis and all_in_one """
        
    # ## create parser
    application_parser = argparse.ArgumentParser(description='classify jobads and extract/match information')

    # ## create subparsers
    """ subparsers = application_parser.add_subparsers()
    subparsers.required = True """

 
    # 2. subparser 'quenfo_py'
    application_parser.add_argument('--classification', action="store_true")
    application_parser.add_argument('--extraction', action="store_true")
    application_parser.add_argument('--matching', action="store_true")
    application_parser.add_argument('--input_path', type = __file_path)
    application_parser.add_argument('--db_mode', choices=['overwrite', 'append'],
                                   default='overwrite')
    
    application_parser.set_defaults(func=manage_app)


    return application_parser

def __file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid file")



# ########## START & FINISH PROGRAM ##########

if __name__ == '__main__':
    start = timer()
    logging.info('\nThe Program started. More information about the process can be found in the file "logger.log".')
    logging.info('\n\n******************************** The program started. ********************************\n')
    print('\n\n******************************** The program started. ********************************\n')
    try:
        parser = get_application_parser()
        arguments = parser.parse_args()
        logging.info(f'The arguments {arguments} are given.')
        logging.info(f'The function {vars(arguments)["func"]} is called.')
    except:
        print(f'Error occurred while parsing for arguments. Use -h flag to get further informations.')
        sys.exit()
    arguments.func(arguments)
    print('Processing done. For further information see logger-file.')
    print('\n\n******************************** The program finished. ********************************\n')
    logging.info('\n\n******************************** The program finished. ********************************\n')
    end = timer()
    print(timedelta(seconds=end-start))
    sys.exit(1)
