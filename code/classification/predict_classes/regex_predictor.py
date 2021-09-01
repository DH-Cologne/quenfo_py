""" Script contains the prediction of classes via regex_classifier. """
# ## Imports
import re
import pandas as pd

# ## Functions
def gen_classes(para: str, regex_clf: pd.DataFrame()) -> list:
    """ Function to predict the class for a cu via regex_classifier
    
    Parameters
    ----------
    para: str
        The content of a ClassifyUnit only slightly preprocessed.

    regex_clf: pd.DataFrame()
        The regex pattern + classes stored in DataFrame.
        
    Returns
    -------
    predicted: list
        The predicted class(es). """

    # Initiate predicted list again for each paragraph
    predicted = list()

    def __compare_matches(class_nr, pattern):
        # check if pattern is in para
        match_result = re.match(pattern, para.lower())
        # captures() saves multiple matches if more than one is found
        try:
            match_result.captures(1)
        except AttributeError:
            pass
        # return None or int(class_nr)
        if match_result == None:
            return None
        else:
            return int(class_nr)

    # check if pattern from regex_clf are in para and return class(es)
    predicted = [__compare_matches(class_nr, pattern) for class_nr, pattern in zip(regex_clf['class_nr'], regex_clf['pattern'])]
    # remove None from list
    predicted = list(filter(None, predicted))
    # remove duplicates from list
    predicted = list(dict.fromkeys(predicted))
    # return list predicted classes for current paragraph
    return predicted