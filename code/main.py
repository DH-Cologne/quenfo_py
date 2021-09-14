""" Main Script of the application. Manages the main components of the tool. Further information for execution can be found in the file readme.md.

PURPOSE: 
    Split JobAds into paragraphs and classify them. Extract/match competences and tools.

INPUT:
        - SQL-Databases containing job-ads (One as Trainingdata and one as Testdata)
OUTPUT:
        - New Table "classify_units" in Testdata with classified paragraphs, list of competences, list of tools.
STRUCTURE:
        Program consists of three major parts:
            a. Textclassification
            b. Information Extraction
            c. Matching
TASKS: 
    a. Textclassification: Split JobAds into paragraphs and classify them:
    Possible classes: 
        1. Selbstvorstellung des ausschreibenden Unternehmens
        2. Beschreibung der Tätigkeit, Angebote an die Bewerberinnen und Bewerber
        3. Anforderungen an die Bewerberin bzw. den Bewerber 
        4. Formalia und Sonstiges
        5: 1&3
        6: 2&3
    b. Information Extraction: 
        b.1 Competences
        b.2 Tools
    c. Matching:
        c.1 Competences
        c.2 Tools
PATHS   --> All paths can be adjusted in the config.yaml, except the input_path (needs to be entered via CLI).

WORKING-DIR: /code

CALLS:
    (ArgumentParser to process CLI-Commands)

    usage: main.py [-h] [--classification] [--extraction] [--matching]
               [--input_path INPUT_PATH] [--db_mode {overwrite,append}]

    classify jobads and extract/match information

    optional arguments:
    -h, --help            show this help message and exit
    --classification
    --extraction
    --matching
    --input_path INPUT_PATH
    --db_mode {overwrite,append}

Example: python main.py --classification --input_path '..\..\quenfo_data\sqlite\orm\text_kernel_orm_2018_03.db' --db_mode overwrite """

# ## Imports
import configuration
import logging
from timeit import default_timer as timer
from datetime import timedelta
import argparse
import sys
import os
import training
import classification
import database
import logger

# ## Initiate Logging-Module
logger.main()
logger.log_main.info("HEllo")

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


def manage_app(args: dict) -> None:

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
        Parser contains 
            a. the three tool parts as options: classification, extraction, matching
            b. input_path argument (use string format!)
            c. db_mode (options: overwrite or append) """
        
    # ## create parser
    application_parser = argparse.ArgumentParser(description='classify jobads and extract/match information')
 
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
        arguments.func(arguments)
        logging.info(f'The function {vars(arguments)["func"]} is called.')
    except TypeError as e:
        print(f'Error {e} occurred while parsing for arguments. Use -h flag to get further informations.')
        sys.exit()
    print('Processing done. For further information see logger-file.')
    print('\n\n******************************** The program finished. ********************************\n')
    logging.info('\n\n******************************** The program finished. ********************************\n')
    end = timer()
    print(timedelta(seconds=end-start))
    sys.exit(1)
