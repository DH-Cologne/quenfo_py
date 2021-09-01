# ## Imports
from . import gen_regex
import pandas as pd

# ## Function
def call_regex_clf() -> pd.DataFrame():
    # Start extraction of regex pattern and classes from given regex file
    regex_clf = gen_regex.start()
    # Return regex classifier
    return regex_clf