# ## Imports
from . import connection

session = None
session2 = None
engine = None
engine2 = None


def get_input_conn():
    global session, engine
    # Get instantiated session object and engine for Input_data
    session, engine = connection.set_testdata()
    

def get_train_conn():
    global session2, engine2
    # Get instantiated session2 object and engine2 for Traindata_data
    session2, engine2 = connection.set_traindata()