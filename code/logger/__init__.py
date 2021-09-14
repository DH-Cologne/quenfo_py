from __future__ import absolute_import
from pathlib import Path
import logging

log_clf = None
log_match = None
log_ie = None
log_main = None


def setup_logger(logger_name, log_file, level=logging.DEBUG):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(threadName)s : %(levelname)s : %(message)s')
    
    fileHandler = logging.FileHandler(log_file, mode='w+')
    fileHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)


def main():
    global log_clf
    global log_match
    global log_ie
    global log_main

    setup_logger('log_clf', Path('logger/logger_classification.log'))
    setup_logger('log_match', Path('logger/logger_matching.log'))
    setup_logger('log_ie', Path('logger/logger_extraction.log'))
    setup_logger('log_main', Path('logger/logger_main.log'))

    log_clf = logging.getLogger('log_clf')
    log_match = logging.getLogger('log_match')
    log_ie = logging.getLogger('log_ie')
    log_main = logging.getLogger('log_main')

if '__main__' == __name__:
    main()