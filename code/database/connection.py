""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from orm_handling.models import Configurations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path


# ## Input-Paths (Testdata and Traindata)
input_path = Configurations.get_input_path()
traindata_path = Configurations.get_traindata_path()

# Create engine with path
engine = create_engine('sqlite:///' + input_path, echo=False)
engine2 = create_engine('sqlite:///' + traindata_path, echo=False)

# Bind engine to recieve a session
Session = sessionmaker(bind=engine)
Session2 = sessionmaker(bind=engine2)

# Instantiate a session object
session = Session()
session2 = Session2()

