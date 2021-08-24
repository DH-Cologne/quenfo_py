""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from orm_handling.models import Configurations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path


# ## Input-Paths
input_path = Configurations.get_input_path()
traindata_path = Configurations.get_traindata_path()


# Create engine with path
engine = create_engine('sqlite:///' + input_path, echo=False)

# Bind engine to recieve a session
Session = sessionmaker(bind=engine)

# Instantiate a session object
session = Session()

engine2 = create_engine('sqlite:///' + traindata_path, echo=False)
Session2 = sessionmaker(bind=engine2)
session2 = Session2()

