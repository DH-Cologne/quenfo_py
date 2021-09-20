""" LOGGING: Script contains logging-related fuctions -> Setup the four different logging-files. 
        a. log_main.log --> for all main related processes and raises.
        b. log_clf.log  --> for all classification related processes and raises.
        c. log_ie.log   --> for all information extraction related processes and raises.
        d. log_match.log--> for all matching related processes and raises. """

# ## Imports
from __future__ import absolute_import
from pathlib import Path
import logging

# ## Set Variables
log_clf = None
log_match = None
log_ie = None
log_main = None

# ## Functions
def __setup_logger(logger_name: str, log_file: Path, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    # no stdout from logging
    l.propagate = False
    formatter = logging.Formatter('%(asctime)s : %(threadName)s : %(levelname)s : %(message)s')
    
    fileHandler = logging.FileHandler(log_file, mode='w+')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)

# Main Function for setup
def main() -> None:
    """ Main logging-function to setup the differnt logging files. """
    # Set globals
    global log_clf, log_match, log_ie, log_main

    # Set logger for specific files
    __setup_logger('log_clf', Path('logger/logger_classification.log'))
    __setup_logger('log_match', Path('logger/logger_matching.log'))
    __setup_logger('log_ie', Path('logger/logger_extraction.log'))
    __setup_logger('log_main', Path('logger/logger_main.log'))

    # Get specific logger
    log_clf = logging.getLogger('log_clf')
    log_match = logging.getLogger('log_match')
    log_ie = logging.getLogger('log_ie')
    log_main = logging.getLogger('log_main')

# Set specific information for logging and stdout. 
def set_infos(spec_logger: logging.Logger, step: str, mode:str) -> None:
    """ Set specific information for logging and stdout depending on step.

    Parameters
    ----------
    spec_logger: logging.Logger
        specific logger obj to log into.
    step: str
        String with the name of the step (e.g. Classification, Extraction or Matching)
    mode: str
        String with the value 'start' or 'finish'"""

    try:
        log_main.info(f'{step} about to {mode}. Further information in {spec_logger}.')
        spec_logger.info(f'\n\n******************************** {step} {mode}ed. ********************************\n')
        print(f'{step} {mode}ed.')
    except Exception as e:
        log_main.warning(f'Error {e} is raised. Continue with program and ignore logging/printing error.')


if '__main__' == __name__:
    main()