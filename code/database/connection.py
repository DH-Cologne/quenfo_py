""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from configuration.config_model import Configurations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ## Input-Paths (Testdata and Traindata)
input_path = Configurations.get_input_path()
traindata_path = Configurations.get_traindata_path()

# Create engine with path
engine = create_engine('sqlite:///' + input_path, echo=False)
engine.execution_options(stream_results=True)
engine2 = create_engine('sqlite:///' + traindata_path, echo=False)
engine2.execution_options(stream_results=True)

# Bind engine to recieve a session
Session = sessionmaker(bind=engine)
Session2 = sessionmaker(bind=engine2)

# Instantiate a session object
session = Session()
session2 = Session2()