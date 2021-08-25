# ## Imports
from . import connection

# Get instantiated session object and engine for Input_data
session = connection.session
engine = connection.engine

# Get instantiated session2 object and engine2 for Traindata_data
session2 = connection.session2
engine2 = connection.engine2