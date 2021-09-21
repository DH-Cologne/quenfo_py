""" Script contains the two functions to manage the database connections. """

# ## Imports
from . import connection
import configuration

# ## Set Variables
session = None
session2 = None
engine = None
engine2 = None


# ## Functions
# Input-Connection
def set_input_conn() -> None:
    """ Function to manage database-connection for input-data.
            a. Set session and engine global
            b. Get input-path from configuration object
            c. Create a connection via input_path and fill session and engine """
    # Set globals
    global session, engine
    # Get input-path from configuration
    input_path = configuration.config_obj.get_input_path()
    # Get instantiated session object and engine for Input_data
    session, engine = connection.create_connection(input_path)


# Traindata-Connection
def set_train_conn() -> None:
    """ Function to manage database-connection for train-data.
            a. Set session2 and engine2 global
            b. Get traindata-path from configuration object
            c. Create a connection via traindata_path and fill session2 and engine2 """
    # Set globals
    global session2, engine2
    # Get traindata-path from configuration
    traindata_path = configuration.config_obj.get_traindata_path()
    # Get instantiated session2 object and engine2 for Traindata_data
    session2, engine2 = connection.create_connection(traindata_path)
