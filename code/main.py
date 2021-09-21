""" MAIN SCRIPT of the application. Manages the main components of the tool. Further information for execution can be found in the file readme.md.

*****************
*** QUENFO_PY ***
*****************

* PURPOSE: 
    Split JobAds into paragraphs and classify them. Extract/match competences and tools.

* INPUT:
        - SQL-Databases containing job-ads (One as Trainingdata and one as Testdata)
* OUTPUT:
        - New Table "classify_units" in Testdata with classified paragraphs, list of competences, list of tools.
* STRUCTURE:
        Program consists of three major parts:
            a. Textclassification
            b. Information Extraction
            c. Matching
* TASKS: 
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

* PATHS: All paths can be adjusted in the config.yaml, except the input_path (needs to be entered via CLI).

* WORKING-DIR: /code

* TESTS: in Module code/tests

* CALLS:
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

CLI-example: python main.py --classification --input_path '..\..\quenfo_data\sqlite\orm\text_kernel_orm_2018_03.db' --db_mode overwrite """

# ## Imports
import configuration
from timeit import default_timer as timer
from datetime import timedelta
import argparse
import sys
import os
import training
import classification
import database
import logger
from pathlib import Path
from information_extraction import extract

# ## Initiate Logging-Module
""" 
Set four different logging-files: 
    a. log_main.log --> for all main related processes and raises.
    b. log_clf.log  --> for all classification related processes and raises.
    c. log_ie.log   --> for all information extraction related processes and raises.
    d. log_match.log--> for all matching related processes and raises."""

logger.main()


# ## Functions

# *** PART 1: Textclassification ***
def start_classification() -> None:
    """ Function to manage the classification step. 
        a. Train or Load model 
        b. Classify JobAd-paragraphs with model """

    # STEP 1: Train or Load Vectorizer, KNN and Regex_clf as Class-object model
    model = training.initialize_model()

    # STEP 2: Start Classification
    classification.classify(model)


# *** PART 2: Information Extraction ***
def start_extraction() -> None:
    extract()


# *** PART 3: Matching ***
def start_matching() -> None:
    pass


# Manage the different parts and set configurations/connections
def manage_app(args: dict) -> None:
    """ Function to 
            a. set configurations with vars from argparser and config.yaml-file. 
            b. establish the database-connections to the traindata-file (config.yaml) and input_path (argparser). 
    
    Parameters
    ----------
    args: dict
        dictionary with the arguments received by argparser. """

    # Get items from dict
    method_args = vars(args)

    # First: set configurations and database-connections
    def __set_all():
        """ Set globals: configuration values and database connections. """
        try:
            configuration.set_config(method_args)
            database.set_train_conn()
            database.set_input_conn()
            logger.log_main.info(f'Configurations set: {configuration.config_obj} and database connections created: \n \
                input_data: {database.session} traindata: {database.session2}')
        except Exception as e:
            logger.log_main.info(
                f'Error {e} occurred. Checkout configurations, argparser and connections to databases.')
            print(f'Error {e} occurred. Checkout configurations, argparser and connections to databases.')
            sys.exit()

    __set_all()

    # Second: Call each part of the application (depending on given argparse arguments)
    def __call_parts():
        # Textclassification
        def __call_clf():
            logger.set_infos(logger.log_clf, 'Classification', 'start')
            start_classification()
            logger.set_infos(logger.log_clf, 'Classification', 'finish')

        # Information Extraction
        def __call_ie():
            logger.set_infos(logger.log_ie, 'Information Extraction', 'start')
            start_extraction()
            logger.set_infos(logger.log_ie, 'Information Extraction', 'finish')

        # Matching
        def __call_match():
            logger.set_infos(logger.log_match, 'Matching', 'start')
            start_matching()
            logger.set_infos(logger.log_match, 'Matching', 'finish')

        # Call part or all depending on argparser
        if method_args['classification']:
            __call_clf()
        if method_args['extraction']:
            __call_ie()
        if method_args['matching']:
            __call_match()
        if not (method_args['classification']) and not (method_args['extraction']) and not (method_args['matching']):
            __call_clf()
            __call_ie()
            __call_match()

    __call_parts()


# ## ArgumentParser

def get_application_parser() -> argparse.ArgumentParser:
    """ Function to generate an ArgumentParser and return given arguments from CLI

    Returns
    ----------
    application_parser : parser
        Parser contains:
            a. the three tool parts as options: classification, extraction, matching (if non is given, call all parts)
            b. input_path argument (use string format!)
            c. db_mode (options: overwrite or append) """

    # ## create parser
    application_parser = argparse.ArgumentParser(description='classify jobads and extract/match information')
    # ## add arguments
    application_parser.add_argument('--classification', action="store_true")
    application_parser.add_argument('--extraction', action="store_true")
    application_parser.add_argument('--matching', action="store_true")
    application_parser.add_argument('--input_path', type=__file_path)
    application_parser.add_argument('--db_mode', choices=['overwrite', 'append'],
                                    default='overwrite')
    # ## set default function
    application_parser.set_defaults(func=manage_app)
    return application_parser

def __file_path(path: str) -> str:
    if os.path.exists(Path(path)):
        return path
    else:
        raise argparse.ArgumentTypeError(f"Readable_file:{path} is not a valid file")


# ########## START & FINISH PROGRAM ##########

if __name__ == '__main__':

    # start timer
    start = timer()
    # set first logging/printing
    logger.log_main.info('\nThe Program started. More information about the process can be found in the logger-files.')
    logger.log_main.info('\n\n******************************** The program started. ********************************\n')
    print('\n\n******************************** The program started. ********************************\n')


    # Check if CLI is used correctly
    def __get_arguments():
        try:
            parser = get_application_parser()
            arguments = parser.parse_args()
            logger.log_main.info(f'The arguments {arguments} are given.')
            logger.log_main.info(f'The function {vars(arguments)["func"]} is called.')
            arguments.func(arguments)
            pass
        except (TypeError, AttributeError) as e:
            print(f'Error {e} occurred while parsing for arguments. Use -h flag to get further informations.')
            sys.exit()


    __get_arguments()

    # set final logging/printing
    logger.log_main.info(
        '\n\n******************************** The program finished. ********************************\n')
    print('Processing done. For further information see logger-files.')
    print('\n\n******************************** The program finished. ********************************\n')
    # finish timer
    end = timer()
    print(f'Runtime of program: {timedelta(seconds=end - start)}.')
    sys.exit()
