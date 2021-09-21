""" Script uses the regex_path to open the regex.txt file and extract pattern/classes. Both are appended to lists and stored in DataFrame. """

# ## Imports
import pandas as pd
from pathlib import Path
from typing import Union
import configuration
import logger

# Set Variables
regex_clf = pd.DataFrame()
class_list = list()
pattern_list = list()
    
# ## Functions
def start() -> pd.DataFrame():
    """ Function to extract regex pattern and classes to fill the regex classifier.
    
    Returns
    -------
    regex_clf: pd.DataFrame
        Dataframe with the columns class_nr and pattern. Contains the values for regex_classifier. """

    # Get regex.txt file from config
    regex_path = configuration.config_obj.get_regex_path()
    # Open and read regex-file. Returns the regex_classifier classes and pattern. 
    class_list, pattern_list = __read_file(regex_path)
    # Store both lists in DataFrame regex_clf
    regex_clf['class_nr'] = class_list
    regex_clf['pattern'] = pattern_list
    # Return regex_classifier
    return regex_clf


def __read_file(regex_path: str) -> Union[list, list]:
    try:
        with open(Path(regex_path), 'rb') as f:
            for line in f.readlines():
                line = [x for x in (line.decode()).split('\t')]
                if not(line[0].__contains__('#')):
                    class_list.append(line[0])
                    pattern_list.append(line[1].replace("\r\n", ""))
                else:
                    continue
            f.close()
    except:
        print(f'Problems occurred while reading file {regex_path}.')
        logger.log_clf.warning(f'Problems occurred while reading file {regex_path}.')
    return class_list, pattern_list