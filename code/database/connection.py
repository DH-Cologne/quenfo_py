""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# ## Input-Paths (TODO: Store in config)

#input_path = os.path.join('..','..', 'traindata_sql.db')
input_path = os.path.join('..','..', 'text_kernel_orm_2018_03.db')

# Create engine with path
engine = create_engine('sqlite:///' + input_path, echo=False)

# Bind engine to recieve a session
Session = sessionmaker(bind=engine)

# Instantiate a session object
session = Session()