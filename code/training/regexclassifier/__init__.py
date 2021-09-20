# ## Imports
from . import gen_regex
import pandas as pd
import logger

# ## Function
def call_regex_clf() -> pd.DataFrame():
    # Start extraction of regex pattern and classes from given regex file
    regex_clf = gen_regex.start()
    # Print/Log status
    if not(regex_clf.empty):
        logger.log_clf.info(f'Regex Classifier is loaded and returned to next processing step.')
        print(f'Regex Classifier is loaded and returned to next processing step.')
    else:
        logger.log_clf.warning(f'Regex Classifier could not be loaded. Continue without it.')
        print(f'Regex Classifier could not be loaded. Continue without it.')
    # Return regex classifier
    return regex_clf