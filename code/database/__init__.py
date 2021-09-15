# ## Imports
from . import connection
import configuration

session = None
session2 = None
engine = None
engine2 = None


def set_input_conn():
    global session, engine
    input_path = configuration.config_obj.get_input_path()
    # Get instantiated session object and engine for Input_data
    session, engine = connection.create_connection(input_path)
    

def set_train_conn():
    global session2, engine2
    traindata_path = configuration.config_obj.get_traindata_path()
    # Get instantiated session2 object and engine2 for Traindata_data
    session2, engine2 = connection.create_connection(traindata_path)